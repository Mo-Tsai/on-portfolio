(function(){
  var imgs=[].slice.call(document.querySelectorAll('.mag-cell img, .plan-section:not(.hidden) img'));
  var srcs=imgs.map(function(i){return i.currentSrc||i.src});
  var lb=document.getElementById('lb');
  var lbImg=document.getElementById('lb-img');
  var lbC=document.getElementById('lb-counter');
  var cur=0;
  function show(i){cur=i;lbImg.src=srcs[cur];lbC.textContent=(cur+1)+' / '+srcs.length;lb.classList.add('open')}
  function close(){lb.classList.remove('open');lbImg.src=''}
  imgs.forEach(function(img,i){img.addEventListener('click',function(){show(i)})});
  [].slice.call(document.querySelectorAll('.thumb-strip .thumb')).forEach(function(t){
    t.addEventListener('click',function(){
      var s=t.querySelector('img').currentSrc||t.querySelector('img').src;
      var i=srcs.findIndex(function(x){return x===s});
      if(i>=0)show(i);else{srcs.push(s);show(srcs.length-1)}
    });
  });
  document.getElementById('lb-close').onclick=close;
  document.getElementById('lb-prev').onclick=function(){cur=(cur-1+srcs.length)%srcs.length;lbImg.src=srcs[cur];lbC.textContent=(cur+1)+' / '+srcs.length};
  document.getElementById('lb-next').onclick=function(){cur=(cur+1)%srcs.length;lbImg.src=srcs[cur];lbC.textContent=(cur+1)+' / '+srcs.length};
  lb.addEventListener('click',function(e){if(e.target===lb)close()});
  document.addEventListener('keydown',function(e){
    if(!lb.classList.contains('open'))return;
    if(e.key==='ArrowLeft')document.getElementById('lb-prev').click();
    if(e.key==='ArrowRight')document.getElementById('lb-next').click();
    if(e.key==='Escape')close();
  });
})();
