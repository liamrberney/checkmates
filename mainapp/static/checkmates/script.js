

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#blah')
                .attr('src', e.target.result)
                .width(400)
                .height(400);
        };

        reader.readAsDataURL(input.files[0]);
    }
}


if(localStorage.getItem('fontSizeToggle') != 'enabled' && localStorage.getItem('fontSizeToggle') != 'disabled'){
    localStorage.setItem('fontSizeToggle','disabled');
    location.reload();
}


let root = document.documentElement
if(localStorage.getItem('fontSizeToggle') == 'enabled'){
    console.log("toggle enabled");
    root.style.setProperty('--font-size', 20 + "px");
    root.style.setProperty('--header-font-size', 25 + "px");
}
else{
    console.log("toggle disabled");
    root.style.setProperty('--font-size', 15 + "px");
    root.style.setProperty('--header-font-size', 20 + "px");
}


function change() {
    let root = document.documentElement;
    
    console.log(root.style.getPropertyValue('--font-size'));
    if (root.style.getPropertyValue('--font-size')=='15px' || root.style.getPropertyValue('--font-size')==''){
        console.log("toggle enabled");
        localStorage.setItem('fontSizeToggle','enabled');
        location.reload();
    }
    else{    
        console.log("toggle disabled");
        localStorage.setItem('fontSizeToggle','disabled');
        location.reload();
    }
    console.log(localStorage.getItem('fontSizeToggle'));
    
};

var synth = window.speechSynthesis;

var inputForm = document.querySelector('form');
var inputTxt = document.querySelector('.txt');
var voiceSelect = document.querySelector('select');


var voices = [];

function populateVoiceList() {
  voices = synth.getVoices().sort(function (a, b) {
      const aname = a.name.toUpperCase(), bname = b.name.toUpperCase();
      if ( aname < bname ) return -1;
      else if ( aname == bname ) return 0;
      else return +1;
  });
  var selectedIndex = voiceSelect.selectedIndex < 0 ? 0 : voiceSelect.selectedIndex;
  voiceSelect.innerHTML = '';
  for(i = 0; i < voices.length ; i++) {
    var option = document.createElement('option');
    option.textContent = voices[i].name + ' (' + voices[i].lang + ')';
    
    if(voices[i].default) {
      option.textContent += ' -- DEFAULT';
    }

    option.setAttribute('data-lang', voices[i].lang);
    option.setAttribute('data-name', voices[i].name);
    voiceSelect.appendChild(option);
  }
  voiceSelect.selectedIndex = selectedIndex;
}

populateVoiceList();
if (speechSynthesis.onvoiceschanged !== undefined) {
  speechSynthesis.onvoiceschanged = populateVoiceList;
}

function speak(){
    if (synth.speaking) {
        console.error('speechSynthesis.speaking');
        return;
    }

    var textFields = document.getElementsByClassName("tts");
    console.log(textFields);
    console.log(textFields.length);
    var text = "";
    for (var i = 0; i < textFields.length; i++) {
        text+=textFields[i].textContent + ". ";
    }

    console.log(text);
    var utterThis = new SpeechSynthesisUtterance(text);
    utterThis.onend = function (event) {
        console.log('SpeechSynthesisUtterance.onend');
    }
    utterThis.onerror = function (event) {
        console.error('SpeechSynthesisUtterance.onerror');
    }
    var selectedOption = "English (America)";//voiceSelect.selectedOptions[0].getAttribute('data-name');
    console.log(selectedOption);
    for(i = 0; i < voices.length ; i++) {
        if(voices[i].name === selectedOption) {
            utterThis.voice = voices[i];
            //console.log(voices[i]);
            break;
        }
    }
    utterThis.pitch = .5;
    utterThis.rate = 1;
    synth.speak(utterThis);
        
    
  
}

inputForm.onsubmit = function(event) {
  event.preventDefault();

  speak();
  console.log(pitch.value);
  console.log(rate.value);
  //console.log(voiceSelect.selectedOptions[0].getAttribute('data-name'));
  inputTxt.blur();
}

function saveEdits(){
    var fullname = document.getElementById('fullname').textContent.trim();
    var email = document.getElementById('email').textContent.trim();
    var bio = document.getElementById('bio').textContent.trim();
    var phonenumber = document.getElementById('phonenumber').textContent.trim();
    var imageurl = document.getElementById('blah').src;
    //fetch("/like/?username="+username)
    console.log(fullname + "\n " + email + "\n" + bio + "\n" + phonenumber + "\n" + imageurl);
    fetch("/saveprofile/?email="+email+"&bio="+bio+"&fullname="+fullname+"&phonenumber="+phonenumber,
    {
        method: 'POST',
        headers:{
            //imageurl': imageurl,
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest' //Necessary to work with request.is_ajax()
        },
        body: JSON.stringify({'imageurl':imageurl})
    });
    //location.reload();
}