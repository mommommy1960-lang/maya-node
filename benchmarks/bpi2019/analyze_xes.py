#!/usr/bin/env python3
"""Streaming first-pass BPI 2019 XES analyzer. Python standard library only."""
import argparse, json, statistics
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime
from pathlib import Path

PUBLISHED_CASES, PUBLISHED_EVENTS = 251734, 1595923

def tag_name(tag):
    return tag.rsplit("}", 1)[-1]

def value(el):
    raw = el.attrib.get("value")
    if raw is None: return None
    kind = tag_name(el.tag)
    try:
        if kind in ("int", "integer"): return int(raw)
        if kind in ("float", "double"): return float(raw)
        if kind == "boolean": return raw.lower() == "true"
    except ValueError:
        pass
    return raw

def attrs(parent):
    return {c.attrib["key"]: value(c) for c in list(parent)
            if c.attrib.get("key") and value(c) is not None}

def timestamp(raw):
    if not isinstance(raw, str): return None
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return dt if dt.tzinfo is not None else None
    except ValueError:
        return None

def summarize(values):
    if not values:
        return {"n": 0, "median_hours": None, "mean_hours": None, "negative_intervals": 0}
    return {"n": len(values), "median_hours": round(statistics.median(values), 3),
            "mean_hours": round(statistics.fmean(values), 3),
            "negative_intervals": sum(v < 0 for v in values)}

def analyze(path):
    cases = events = missing_ids = missing_activities = missing_times = duplicates = 0
    seen_ids, activities, categories, variants, attribute_presence = set(), Counter(), Counter(), Counter(), Counter()
    numeric_event_attributes = Counter()
    min_ts = max_ts = None
    gr_invoice, invoice_clear = [], []
    for _, trace in ET.iterparse(str(path), events=("end",)):
        if tag_name(trace.tag) != "trace": continue
        cases += 1
        ta = attrs(trace)
        cid = ta.get("concept:name")
        if not cid or cid in seen_ids: missing_ids += 1
        elif cid: seen_ids.add(cid)
        categories[str(ta.get("Item Category") or ta.get("Item Type") or "UNCLASSIFIED")] += 1
        for k in ta: attribute_presence["trace:"+k] += 1
        ordered, fingerprints = [], set()
        for ev in list(trace):
            if tag_name(ev.tag) != "event": continue
            events += 1
            ea = attrs(ev)
            for k, v in ea.items():
                attribute_presence["event:"+k] += 1
                if isinstance(v, (int, float)) and not isinstance(v, bool): numeric_event_attributes[k] += 1
            act = ea.get("concept:name")
            if not act: missing_activities += 1; act = "MISSING_ACTIVITY"
            act = str(act); activities[act] += 1
            raw_ts = ea.get("time:timestamp"); ts = timestamp(raw_ts)
            if ts is None: missing_times += 1
            else:
                min_ts = ts if min_ts is None or ts < min_ts else min_ts
                max_ts = ts if max_ts is None or ts > max_ts else max_ts
            fp = (act, str(raw_ts), json.dumps(ea, sort_keys=True, default=str))
            if fp in fingerprints: duplicates += 1
            fingerprints.add(fp); ordered.append((ts, act))
        ordered = sorted((x for x in ordered if x[0] is not None), key=lambda x:x[0])
        seq = tuple(a for _, a in ordered)
        if seq: variants[seq] += 1
        gr = [t for t,a in ordered if "Record Goods Receipt" in a]
        inv = [t for t,a in ordered if "Record Invoice Receipt" in a]
        clr = [t for t,a in ordered if "Clear Invoice" in a]
        if gr and inv: gr_invoice.append((min(inv)-min(gr)).total_seconds()/3600)
        if inv and clr: invoice_clear.append((min(clr)-min(inv)).total_seconds()/3600)
        trace.clear()
    return {
      "dataset":"BPI Challenge 2019","source_file":Path(path).name,"cases":cases,"events":events,
      "published_reference_counts":{"cases":PUBLISHED_CASES,"events":PUBLISHED_EVENTS,
        "case_count_matches":cases==PUBLISHED_CASES,"event_count_matches":events==PUBLISHED_EVENTS},
      "data_quality":{"missing_or_duplicate_case_ids":missing_ids,"missing_activity_names":missing_activities,
        "missing_or_unparseable_timestamps":missing_times,"duplicate_event_fingerprints_within_case":duplicates},
      "timestamp_range":{"min":min_ts.isoformat() if min_ts else None,"max":max_ts.isoformat() if max_ts else None},
      "item_categories":dict(categories.most_common()),"activity_counts":dict(activities.most_common()),
      "top_25_ordered_variants":[{"count":n,"activities":list(s)} for s,n in variants.most_common(25)],
      "throughput_diagnostics":{"goods_receipt_to_first_invoice":summarize(gr_invoice),
        "first_invoice_to_first_clear":summarize(invoice_clear)},
      "attribute_presence_counts":dict(attribute_presence.most_common()),
      "numeric_event_attributes":dict(numeric_event_attributes.most_common()),
      "interpretation_limits":[
        "Event-log deviations are not automatically policy violations or losses.",
        "Intervals use first matching activity timestamps; they are not invoice-to-receipt matching.",
        "No independent ground-truth dispositions are supplied by this analyzer.",
        "This dataset does not contain separate WMS, carrier, and customer-support source feeds.",
        "No causation, fraud, recoverable value, savings, or ROI is inferred.",
        "Timezone-less timestamps are counted as unparseable rather than silently assigned a timezone."
      ]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("xes_file"); p.add_argument("--output",default="bpi2019_analysis.json")
    a=p.parse_args(); result=analyze(a.xes_file)
    Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("cases","events","published_reference_counts","data_quality","timestamp_range")},indent=2))

if __name__=="__main__": main()
