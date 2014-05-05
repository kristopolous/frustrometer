self.frust = self.frust || {
  // The cut off before showing the thermometer
  thermo_above: 0.30,

  // The neutral score
  start_score: 0.25,

  // The cut off before showing the snarky comments
  title_above: 0.05,

  // polling interval for the textareas
  ival_poll: 200

  site: (document.location.host == 'local.frust.me') ? 
    '//local.' : '//www.'
};

(function(){  

  self.frust.setuuid = function(uuid) {
    self.frust.uuid = uuid;
  }

  // a Very very cheap dom builder.
  function d(attrib, type) {
    var obj = document.createElement(type || 'div'), key;

    for(key in attrib) {
      if(key == 'html') {
        obj.innerHTML = attrib[key];
      } else {
        obj.setAttribute(key, attrib[key]);
      }
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
    obj.thermo.style.height = res.score + 'em';//(res.score > frust.thermo_above) ? 'block' : 'none';
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

    if(Math.round(deltaScore / 7) != 0) {
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

  function post(url, data, cb, force) {
    if(post.lock != true || force) {
      if(!force) {
        post.lock = true;
      }

      var request = new XMLHttpRequest();
      request.open('POST', url, true);
      request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
      request.onreadystatechange = function() {
        if (request.readyState == 4) {
          var res = JSON.parse(request.responseText);
          cb(res);
          if(!force) {
            post.lock = false;
          }
        }
      }

      request.send(JSON.stringify(data));
    }
  }

  function update(content, obj) {
    // We can't move forward without a uuid regardless. (future)
    // if (!self.frust.uuid) {
    //  return;
    // }

    post(
      frust.site + "frust.me/analyze",
      {data: content},
      function(res) { setLevel(res, obj); }
    );
  }

  function autocorrect() {
    console.log(this, arguments);
  }

  function faveit() {
    console.log(this, arguments);
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
        <a class='autocorrect'>Auto-correct</a>
        <a class='undo'>undo</a>
        <a class='favorite'>&#9733;</a>
      </div>
    </div>
    */
    var 
      wrapper = d({'class': 'frustrometer'}),
        // textarea
        casing = d({"class": "thermometer-casing"}),
          thermo = d({"class": "thermometer"}),
            temp = d({"class": "temp"}),
          title = d({"class": "thermometer-title"}),
          auto = d({"class": "autocorrect", html: "auto-correct"}, "a"),
          star = d({"title": "Submit as an example", "class": "favorite", html: "&#9733;"}, "a");

    // self.ta = ta;
    thermo.appendChild(temp);
    casing.appendChild(thermo);
    casing.appendChild(title);
    casing.appendChild(auto);
    casing.appendChild(star);

    auto.onclick = autocorrect;
    star.onclick = faveit;

    thermo.style.width = ta.offsetWidth + "px";

    // wrap this 
    ta.parentNode.replaceChild(wrapper, ta);
    ta = wrapper.appendChild(ta);
    wrapper.appendChild(casing);
    thermo.style.height = "0.01em";

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
        href: frust.site + "frust.me/style.css"
      }, 'link')
    );

    for(var ix = 0; ix < taList.length; ix++) {
      listenTo(taList[ix], ix); 
    }
  }
})();
