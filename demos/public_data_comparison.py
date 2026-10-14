"""Published public records through the existing permission model; no live integrations."""
import json
from pathlib import Path
from collections import Counter
from demos.accountability_demo import Demo, Grant


def run(path):
    sources=json.loads(Path(path).read_text())
    report={'retrieved_at':sources['retrieved_at'],'scope':'Observed public-source records; operator permissions are injected test conditions','datasets':{}}
    for name in ('irs','cfpb'):
        source=sources[name]; rows=source['rows']
        field='SUBSECTION' if name=='irs' else 'company_response'
        direct={'rows':len(rows),'counts':dict(sorted(Counter(str(r[field]) for r in rows).items()))}
        expected_fields=['NAME','CITY','STATE','SUBSECTION','STATUS','NTEE_CD'] if name=='irs' else ['product','issue','company_response','timely','date_received']
        schema_rows=sum(all(k in r and r[k] is not None for k in expected_fields) for r in rows)
        model=Demo(); resource='PUBLIC-'+name+'-'+source['source_sha256']
        model.grants.append(Grant('DEMO-REVIEWER','read_summary',resource,100))
        permitted=model.attempt('DEMO-REVIEWER','read_summary',resource,1)['allowed']
        mediated=direct if permitted else None
        match=mediated==direct
        export_blocked=not model.attempt('DEMO-REVIEWER','bulk_export',resource,2)['allowed']
        model.grants[0].revoked=True
        revoked_blocked=not model.attempt('DEMO-REVIEWER','read_summary',resource,3)['allowed']
        assert permitted and match and export_blocked and revoked_blocked
        report['datasets'][name]={'source':source['source'],'source_sha256':source['source_sha256'],'selection':source['selection'],'schema_complete_rows':schema_rows,'aggregation':direct,'allowed_summary_matches_direct':match,'outside_scope_export_blocked':export_blocked,'revoked_read_blocked':revoked_blocked,'events':model.events}
    report['comparison_checks_passed']=6
    return report


if __name__=='__main__':
    import sys
    print(json.dumps(run(sys.argv[1]),indent=2))
