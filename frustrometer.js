(function(){  

  function d(attrib, type) {
    type = type || 'div';
    var obj = document.createElement(type);

    for(var key in attrib) {
      if(key == "innerHTML") {
        obj[key] = attrib[key];
      } else {
        obj.setAttribute(key, attrib[key]);
      }
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
    29: "You're good at chess, right?",
    32: "Assertive and confident.",
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
  };

  function setLevel(rating, obj) {
    if (rating < 1) { 
      rating *= 100;
    } 
    for(var level in words) {
      if (rating <= level) {
        obj.title.innerHTML = words[level];
        break;
      }
    }

    obj.temp.style.width = ( 100 - rating ) + "%";
  }

  function update(content, obj) {
    var request;

    if(update.lock != true) {
      update.lock = true;
      console.log(content);

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

  function wrap(what) {
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
          thermometer = d({"class": "thermometer"}),
            temp = d({"class": "temp"}),
          title = d({"class": "thermometer-title"});

    thermometer.appendChild(temp);
    casing.appendChild(thermometer);
    casing.appendChild(title);

    // wrap this 
    what.parentNode.replaceChild(wrapper, what);
    what = wrapper.appendChild(what);
    wrapper.appendChild(casing);

    return {
      temp: temp,
      ta: what,
      title: title
    } 
  }

  function listenTo(ta) {
    var content, obj = wrap(ta);

    setInterval(function() {
      var text = obj.ta.value;

      if(text != content && (text.substr(-1).match(/[\ !?\.]/) || text.length == 0)) {
        content = text;
        update(content, obj); 
      }
    }, 200);
  }

  window.onload = function() {
    var 
      taList = document.getElementsByTagName('textarea'), 
      ix;

    for(ix = 0; ix < taList.length; ix++) {
      listenTo(taList[ix]); 
    }
  }
})();
