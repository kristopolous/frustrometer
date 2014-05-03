self.frust = self.frust || {
  // The cut off before showing the thermometer
  thermo_above: 0.30,

  // The neutral score
  start_score: 0.25,

  // The cut off before showing the snarky comments
  title_above: 0.05,

  // polling interval for the textareas
  ival_poll: 200
};

(function(){  

  self.frust.setuuid = function(uuid) {
    self.frust.uuid = uuid;
  }

  // a Very very cheap dom builder.
  function d(attrib, type) {
    var obj = document.createElement(type || 'div'), key;

    for(key in attrib) {
      obj.setAttribute(key, attrib[key]);
    }

    return obj;
  }

  function setLevel(res, obj) {
    var deltaScore = Math.floor(1000 * (res.score - obj.score)),
      start = 40,
      sum = 0,
      color = Math.min(255, Math.abs(deltaScore)),
      ix = start,
      div = d({'class': 'score'});

    obj.score = res.score;
    obj.title.style.display = (res.score > frust.title_above) ? 'block' : 'none';
    obj.thermo.style.display = (res.score > frust.thermo_above) ? 'block' : 'none';
    obj.temp.style.width = (1 - res.score) * 100  + "%";
    obj.title.innerHTML = res.snark;

    if(deltaScore > 0) {
      div.style.color = "rgb(" + [ color , 0 , 0 ].join(',') + ")";
      div.innerHTML = "+" + deltaScore;
    } else {
      div.innerHTML = deltaScore;
      div.style.color = "rgb(" + [ 0, Math.min(color * 3, 255) , 0 ].join(',') + ")";
    }
    // color < 255
    div.style.fontSize = Math.max(1, Math.sqrt(color / 20)) + "em";

    if(round(deltaScore / 5) != 0) {
      obj.wrapper.appendChild(div);
      var ival = setInterval(function(){
        ix--;
        sum += ix;
        div.style.bottom = (sum / 10) + "px";
        div.style.opacity = ix / start;
        if(ix < 0) { 
          obj.wrapper.removeChild(div);
          clearInterval(ival);
        }
      }, 15);
    }
  }

  function update(content, obj) {
    // We can't move forward without a uuid regardless. (future)
    // if (!self.frust.uuid) {
    //  return;
    // }

    var request;

    if(update.lock != true) {
      update.lock = true;

      request = new XMLHttpRequest();
      request.open('POST', "//frust.me/analyze", true);
      request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
      request.onreadystatechange = function() {
        if (request.readyState == 4) {
          var res = JSON.parse(request.responseText);
          setLevel(res, obj);
          update.lock = false;
        }
      }

      request.send(JSON.stringify({
        // may be needed for xdom
        // with older browsers (future)
        // uuid: frust.uuid,
        data: content
      }));
    }
  }

  function wrap(ta) {
    /*
    <div class='frustrometer'>
      <textarea></textarea>
      <div class='thermometer-casing'>
        <div class='thermometer'>
          <div class='temp'></div>
        </div>
        <div class='thermometer-title'>Waiting... </div>
      </div>
    </div>
    */
    var 
      wrapper = d({'class': 'frustrometer'}),
        // textarea
        casing = d({"class": "thermometer-casing"}),
          thermo = d({"class": "thermometer"}),
            temp = d({"class": "temp"}),
          title = d({"class": "thermometer-title"});

    // self.ta = ta;
    thermo.appendChild(temp);
    casing.appendChild(thermo);
    casing.appendChild(title);
    thermo.style.width = ta.offsetWidth + "px";

    // wrap this 
    ta.parentNode.replaceChild(wrapper, ta);
    ta = wrapper.appendChild(ta);
    wrapper.appendChild(casing);
    thermo.style.display = 'none';

    return {
      score: frust.start_score,
      wrapper: wrapper,
      thermo: thermo,
      temp: temp,
      ta: ta,
      title: title
    } 
  }

  function listenTo(ta) {
    var content = false, obj = wrap(ta);

    setInterval(function() {
      var text = obj.ta.value;

      obj.thermo.style.width = obj.ta.offsetWidth;

      if(text != content && (text.substr(-1).match(/[\ !?\.]/) || text.length == 0)) {
        // This prevents an initial call from going out for every empty container
        if(text.length == 0 && content == false) {
          return;
        }
        content = text;
        update(content, obj); 
      }
    }, frust.ival_poll);
  }

  window.onload = function() {
    var taList = document.getElementsByTagName('textarea');

    document.body.appendChild(
      d({
        type: 'text/css',
        rel: 'stylesheet',
//        href: 'style.css'
        href: '//frust.me/style.css'
      }, 'link')
    );

    for(var ix = 0; ix < taList.length; ix++) {
      listenTo(taList[ix], ix); 
    }
  }
})();
