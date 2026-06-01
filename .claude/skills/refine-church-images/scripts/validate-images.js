const https=require('https'), http=require('http');
const d=JSON.parse(require('fs').readFileSync('docs/data/churches.json','utf8'));
const fx=d.churches.filter(c=>/Fredericksburg/i.test(c.address||''));
function head(url){return new Promise(res=>{
  let u; try{u=new URL(url);}catch(e){return res({ok:false,why:'badurl'});}
  const lib=u.protocol==='http:'?http:https;
  const req=lib.request(url,{method:'GET',headers:{'User-Agent':'Mozilla/5.0','Range':'bytes=0-2048'},timeout:8000},r=>{
    const ct=r.headers['content-type']||''; const cl=parseInt(r.headers['content-length']||'0',10);
    let buf=[]; r.on('data',c=>buf.push(c)); r.on('end',()=>{
      const b=Buffer.concat(buf);
      // PNG/JPEG dimension sniff
      let w=0,h=0;
      if(b[0]===0x89&&b[1]===0x50){ w=b.readUInt32BE(16); h=b.readUInt32BE(20); } // PNG
      res({ok:r.statusCode<400, status:r.statusCode, ct, cl, w, h});
    });
  });
  req.on('error',()=>res({ok:false,why:'neterr'})); req.on('timeout',()=>{req.destroy();res({ok:false,why:'timeout'});}); req.end();
});}
(async()=>{
  const flags=[];
  for(const c of fx){
    for(const [field,url] of [['logo',c.image_thumb],['hero',c.image_url]]){
      if(!url||!/^https?:/.test(url))continue;
      const r=await head(url);
      let flag=null;
      if(!r.ok) flag='BROKEN('+(r.status||r.why)+')';
      else if(!/image|octet-stream/.test(r.ct)) flag='NOT-IMAGE('+r.ct.slice(0,20)+')';
      else if(field==='logo'&&r.w&&r.w<48) flag='TINY('+r.w+'x'+r.h+')';
      if(flag) flags.push({name:c.name,slug:c.slug||c.id,field,flag,url:url.slice(0,55)});
      await new Promise(s=>setTimeout(s,150));
    }
  }
  console.log('=== Fredericksburg image validation: '+flags.length+' flagged ===');
  for(const f of flags) console.log('  ['+f.field+'] '+f.flag.padEnd(22)+' '+f.name.slice(0,30).padEnd(30)+' '+f.url);
})();
