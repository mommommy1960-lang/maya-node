package org.civiccontinuum.maya;
import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.*;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

public class MainActivity extends Activity {
 private LinearLayout column;
 private String approvedReport;
 private static final int EXPORT=11;
 private static final String SITE="https://maya-working-workflow-lab.myqueen1960.chatgpt.site/";
 private static final String REPORT="CIVIC CONTINUUM | MAYA NODE\nFICTIONAL NATIVE DEMONSTRATION\n\nPayment DEMO-P1: USD 100.00 received. Source: invented bank row BANK-1.\nAllocation DEMO-A1: USD 70.00 to rent DEMO-C1. Source: invented allocation ALLOC-1.\nAllocation DEMO-A2: USD 20.00 to water DEMO-C2. Source: invented allocation ALLOC-2.\nUSD 10.00 remains unallocated in the supplied example. It is unexplained, not confirmed loss.\n\nDelivery DEMO-D1: 100 bags planned; 80 dispatched; 60 recorded received. 20 dispatched bags lack a receiving entry. This does not establish theft. Source: invented dispatch SHIP-1 and receiving REC-1.\n\nNext action: ask an authorized reviewer for allocation and receiving evidence. No message, external update or payment is performed.\n\nAll facts and references in this native demonstration are fictional. This report is a teaching example, not independently verified company evidence.\n";
 @Override public void onCreate(Bundle state){super.onCreate(state);home();}
 private void screen(){approvedReport=null;ScrollView scroll=new ScrollView(this);column=new LinearLayout(this);column.setOrientation(LinearLayout.VERTICAL);column.setPadding(28,60,28,40);column.setBackgroundColor(Color.rgb(236,245,253));scroll.addView(column);setContentView(scroll);}
 private void text(String value,int size){TextView t=new TextView(this);t.setText(value);t.setTextSize(size);t.setTextColor(Color.rgb(28,60,86));t.setPadding(0,12,0,16);column.addView(t);}
 private Button button(String title,View.OnClickListener action){Button b=new Button(this);b.setText(title);b.setAllCaps(false);b.setOnClickListener(action);column.addView(b);return b;}
 private void open(String url){try{startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(url)));}catch(Exception e){Toast.makeText(this,"A browser is needed for the online workspace.",Toast.LENGTH_LONG).show();}}
 private void home(){screen();text("MAYA NODE",30);text("Follow the evidence. Keep the human in charge.",21);text("Civic Continuum • Android demonstration 0.1\nNative payment and delivery example works without internet. Your hosted account opens in your browser for sign-in and saved records.",16);button("Trace a payment — native demo",v->demo());button("Open my online Maya workspace",v->open(SITE));button("Read the current public guide",v->open("https://github.com/mommommy1960-lang/maya-node/blob/main/MAYA_ACCOUNTABILITY_BUSINESS_POLICY.md"));text("Early access: fictional data only. No billing, bank access, company connector, email sending or employee decisions. This is not a Play Store release.",14);}
 private String digest(String input){try{byte[] bytes=MessageDigest.getInstance("SHA-256").digest(input.getBytes(StandardCharsets.UTF_8));StringBuilder out=new StringBuilder();for(byte b:bytes)out.append(String.format("%02x",b & 255));return out.toString();}catch(Exception e){throw new IllegalStateException(e);}}
 private void demo(){screen();text("Every payment needs a story",27);text(REPORT,17);text("Exact report SHA-256:\n"+digest(REPORT),12);text("Do you approve saving this exact demonstration report? Approval does not authorize a business-system fix or a message.",17);CheckBox consent=new CheckBox(this);consent.setText("I reviewed the full report above");column.addView(consent);Button approve=button("Yes — approve and choose where to save",v->{if(!consent.isChecked())return;approvedReport=REPORT;Intent i=new Intent(Intent.ACTION_CREATE_DOCUMENT);i.addCategory(Intent.CATEGORY_OPENABLE);i.setType("text/plain");i.putExtra(Intent.EXTRA_TITLE,"maya-approved-demo-report.txt");startActivityForResult(i,EXPORT);});approve.setEnabled(false);consent.setOnCheckedChangeListener((b,checked)->approve.setEnabled(checked));button("No — do not save",v->{approvedReport=null;home();});text("Any later report change needs a fresh review. App restart clears pending approval. No report is sent anywhere by Maya.",14);}
 @Override protected void onActivityResult(int request,int result,Intent data){super.onActivityResult(request,result,data);String pending=approvedReport;approvedReport=null;if(request!=EXPORT||result!=RESULT_OK||data==null||data.getData()==null||pending==null)return;try(OutputStream out=getContentResolver().openOutputStream(data.getData())){if(out==null)throw new Exception("No output stream");out.write((pending+"\nHuman approved this exact report for local export.\nSHA-256: "+digest(pending)+"\n").getBytes(StandardCharsets.UTF_8));Toast.makeText(this,"Approved fictional report saved.",Toast.LENGTH_LONG).show();}catch(Exception e){Toast.makeText(this,"Save could not be confirmed.",Toast.LENGTH_LONG).show();}}
}
