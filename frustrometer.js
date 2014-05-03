(function(){  

  // a Very very cheap dom builder.
  function d(attrib, type) {
    var obj = document.createElement(type || 'div'), key;

    for(key in attrib) {
      obj.setAttribute(key, attrib[key]);
    }

    return obj;
  }

  var words = {
    1: "Not enough information... :-(",
    2: "Lick those boots!",
    4: "You appear to be groveling.",
    6: "Walking on eggshells?",
    8: "Apologizing for something?",
    10: "Is this a job interview?",
    12: "Just delightful.",
    14: "Quite polite.",
    16: "So charming!",
    18: "You're doing fine.",
    20: "Such diplomatic prose!",
    23: "Nothing wrong with this.",
    26: "Tactful like a chess game.",
    29: "Not too worried yet...",
    32: "Assertive and confident?!",
    35: "Forward and direct.",
    38: "What's your goal?",
    40: "Blunt. Is that what you want?",
    42: "What's your desired impact?",
    44: "Editing is a great idea.",
    46: "Having a bad day?",
    48: "Different wording?",
    50: "Starting to get saucy?",
    52: "Being a bit snippy?",
    54: "Approach this from a different angle.",
    56: "Rather imposing.",
    58: "Would YOU like to receive this?",
    60: "A bit too aggressive.",
    62: "Really, what will you gain from posting this?",
    64: "Step back for a few minutes.",
    66: "Maybe you shouldn't say anything?",
    68: "Read it outloud to yourself.",
    70: "Very contemptuous. Breath in...",
    72: "Perhaps finish this tomorrow?",
    74: "That's flippant and combative!",
    76: "People Will read this you know, right?",
    78: "Danger Will Robinson!",
    80: "You are crossing the Rubicon.",
    82: "What Audacious Language!", 
    84: "Careful careful...",
    86: "You may be offending many people here.",
    88: "These are fighting words.",
    90: "You're starting fires here.",
    92: "This is a bad idea.",
    94: "You can't be serious...",
    96: "The bridges are burning.",
    98: "1, 2, 3, 4 I declare War!",
    100: "Pack up your things and leave the building."
  }, 
  // only show above this amount
  showabove = 0.30;

  function setLevel(rating, obj) {
    obj.title.style.display = (rating > 0.05) ? 'block' : 'none';
    obj.thermo.style.display = (rating > showabove) ? 'block' : 'none';

    rating *= 100;
    obj.temp.style.width = ( 100 - rating ) + "%";

    for(var level in words) {
      if (rating <= level) {
        obj.title.innerHTML = words[level];
        return;
      }
    }
  }

  function update(content, obj) {
    var request;

    if(update.lock != true) {
      update.lock = true;

      request = new XMLHttpRequest();
      request.open('POST', "//" + document.location.hostname + "/cgi", true);
      request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
      request.onreadystatechange = function() {
        if (request.readyState == 4) {
          var res = JSON.parse(request.responseText);
          setLevel(res.score, obj);
          update.lock = false;
        }
      }
      request.send(content);
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

    thermo.appendChild(temp);
    casing.appendChild(thermo);
    casing.appendChild(title);
    thermo.style.width = ta.offsetWidth;

    // wrap this 
    ta.parentNode.replaceChild(wrapper, ta);
    ta = wrapper.appendChild(ta);
    wrapper.appendChild(casing);
    thermo.style.display = 'none';

    return {
      thermo: thermo,
      temp: temp,
      ta: ta,
      title: title
    } 
  }

  function listenTo(ta) {
    var content, obj = wrap(ta);

    setInterval(function() {
      var text = obj.ta.value;

      obj.thermo.style.width = obj.ta.offsetWidth;

      if(text != content && (text.substr(-1).match(/[\ !?\.]/) || text.length == 0)) {
        content = text;
        update(content, obj); 
      }
    }, 200);
  }

  window.onload = function() {
    var taList = document.getElementsByTagName('textarea');

    for(var ix = 0; ix < taList.length; ix++) {
      listenTo(taList[ix]); 
    }
  }
})();
