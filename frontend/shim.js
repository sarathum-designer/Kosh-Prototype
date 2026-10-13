/* Self-hosted bridge: gives the front end the same `claude.use()` surface it has inside a Claude artifact,
   backed by the Kosh API. Inside an artifact this file is not loaded. */
(function(){
  if (window.claude) return;
  function sample(input, opts){
    opts = opts || {};
    return fetch("/api/sample", {method:"POST", headers:{"content-type":"application/json"}, body:JSON.stringify({input:input}), signal:opts.signal})
      .then(function(r){ return r.json().then(function(j){ if(!r.ok) throw {code:j.error||"upstream_error", message:j.message||"error"}; return j; }); })
      .then(function(j){ if(opts.onText) opts.onText({text:j.text, delta:j.text}); return {text:j.text, truncated:false, modelTierApplied:"default"}; },
            function(e){ if(e && e.name==="AbortError") throw {code:"cancelled"}; throw e && e.code ? e : {code:"upstream_error", message:String(e)}; });
  }
  sample.json = function(input, opts){ return sample(input, opts).then(function(r){ var m=r.text.match(/[\[{][\s\S]*[\]}]/); if(!m) throw {code:"invalid_json", text:r.text}; return JSON.parse(m[0]); }); };
  var downloads = { save: function(req){ var blob = req.data instanceof Blob ? req.data : new Blob([req.data], {type:"text/markdown"}); var a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download=req.filename; document.body.appendChild(a); a.click(); setTimeout(function(){URL.revokeObjectURL(a.href); a.remove();}, 1000); return Promise.resolve({status:"saved"}); } };
  window.claude = { use: function(name){ return Promise.resolve(name==="sample" ? sample : name==="downloads" ? downloads : null); } };
})();
