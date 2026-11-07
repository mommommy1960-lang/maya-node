import {ReservationLedger} from "./reservation-ledger.mjs";
const [file,id]=process.argv.slice(2);
const l=new ReservationLedger(file);
try {console.log(l.reserveBundle({id,items:[{resourceId:"food",quantity:5},{resourceId:"freezer",quantity:5},{resourceId:"truck",quantity:1}],expiresAt:200},100));}finally{l.close();}
