import {createService} from './service.mjs';
import {D1Store} from './d1-store.mjs';
// Route API requests here inside the Site's Worker, after platform dispatch.
export async function handleMayaAPI(request,env){
  if(!env.DB)return Response.json({error:'Maya database unavailable'},{status:503,headers:{'Cache-Control':'no-store'}});
  return createService({store:new D1Store(env.DB)})(request,env);
}
