(function( $ ) {
    $.widget( "custom.combobox", {
      _create: function() {
        this.wrapper = $( "<span>" )
          .addClass( "custom-combobox" )
          .insertAfter( this.element );
 
        this.element.hide();
        this._createAutocomplete();
        this._createShowAllButton();
      },
 
      _createAutocomplete: function() {
        var selected = this.element.children( ":selected" ),
          value = selected.val() ? selected.text() : "";
 
        this.input = $( "<input>" )
          .appendTo( this.wrapper )
          .val( value )
          .attr( "title", "" )
          .addClass( "custom-combobox-input ui-widget ui-widget-content ui-state-default ui-corner-left" )
          .autocomplete({
            delay: 0,
            minLength: 0,
            source: $.proxy( this, "_source" ),
            select: function(event, ui) {
              var ul = document.getElementById("friends_added");
              var li = document.createElement("li");
              
              var regExp = /(\d+)/g;
              var friend_uid = regExp.exec(ui.item.value);

              var a = document.createElement("a");
              a.textContent = "x ";
              a.setAttribute('href', "");
              a.setAttribute("id", "remove_" + friend_uid[0]);

              li.appendChild(a);
              li.appendChild(document.createTextNode(ui.item.value));
              li.setAttribute("id", friend_uid[0]);
              ul.appendChild(li);

              $('a[id^="remove_"]').click(function (e) {
                e.preventDefault();
                var regExp = /_(.*)/g;
                var remove_uid = regExp.exec(this.id)
                $( "#" + remove_uid[1] ).remove();
              });

            }
          });
 
        this._on( this.input, {
          autocompleteselect: function( event, ui ) {
            ui.item.option.selected = true;
            this._trigger( "select", event, {
              item: ui.item.option
            });
          },
 
          autocompletechange: "_removeIfInvalid"
        });
      },

      _createShowAllButton: function() {
        var input = this.input;
        $(".add_button").click(function () {
          input.autocomplete( "search", "" );
        });

      },
 
      _source: function( request, response ) {
        var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
        response( this.element.children( "option" ).map(function() {
          var text = $( this ).text();
          if ( this.value && ( !request.term || matcher.test(text) ) )
            return {
              label: text,
              value: text,
              option: this
            };
        }) );
      },
 
      _removeIfInvalid: function( event, ui ) {
 
        // Selected an item, nothing to do
        if ( ui.item ) {
          return;
        }
 
        // Search for a match (case-insensitive)
        var value = this.input.val(),
          valueLowerCase = value.toLowerCase(),
          valid = false;
        this.element.children( "option" ).each(function() {
          if ( $( this ).text().toLowerCase() === valueLowerCase ) {
            this.selected = valid = true;
            return false;
          }
        });
 
        // Found a match, nothing to do
        if ( valid ) {
          return;
        }
 
        // Remove invalid value
        this.input
          .val( "" );
        this.element.val( "" );
        this.input.autocomplete( "instance" ).term = "";
      },
 
      _destroy: function() {
        this.wrapper.remove();
        this.element.show();
      }
    });
  })( jQuery );
 
$(function() {
  $( "#combobox" ).combobox();
});

var THEarray;

function compareFinished(sched){
    console.log("SCHEDULE: " + sched);
    THEarray = JSON.parse(sched);
    for(var i = 0; i<THEarray.length; i++){
        for(var j = 0; j<THEarray[i].length; j++){
            for(var k = 0; k<THEarray[i][j].length; k++){
                THEarray[i][j][k] = (THEarray[i][j][k] - 29).toString();
            }
        }
    }
    console.log(THEarray);
    var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];

  var now = new Date();
  var day = days[ now.getDay() ];
  var date = now.getDate();
  var month = months[ now.getMonth() ];
  var year = now.getFullYear();

  var day_div = document.getElementById("day");
  day_div.innerHTML = day.toUpperCase();

  var date_div = document.getElementById("date");
  date_div.innerHTML = "- " + month + " " + date + " " + year + " -";
    var cur = date_div.innerHTML.split(" ");
    var d = new Date(cur[3], months.indexOf(cur[1]), cur[2]);
    updateScheduleInfo(d.getDay() - 1, THEarray[d.getDay() - 1]); // Subtract one because Monday = 0 in function
}

function wipeDeBoard(){
    var time_ids = $('#schedule_view tr td').map(function(i,n) {
    return $(n).attr('id');
    }).get();

    var y;
    for (y = 0; y < time_ids.length; ++y) {
      var time = time_ids[y];
      var highlight = document.getElementById(time);
      highlight.style.backgroundColor = "#e2e2e2";
      highlight.style.fontFamily = "Montserrat-Light, sans-serif";
    }
}

function updateScheduleInfo (day, intersects) {
  wipeDeBoard();
  var days = ['Monday','Tuesday','Wednesday','Thursday','Friday'];
  if (days[day].toUpperCase() == document.getElementById("day").innerHTML) {

    var x;
    for (x = 0; x < intersects.length; ++x) {

      var interval = intersects[x];
      var begin = interval[0];
      var end = interval[1];

      var time_ids = $('#schedule_view tr td').map(function(i,n) {
      return $(n).attr('id');
      }).get();

      var y;
      for (y = 0; y < time_ids.length; ++y) {
        var time = time_ids[y];

        if (time >= begin && time <= end) {
          var highlight = document.getElementById(time);
          highlight.style.backgroundColor = "#e1c83d";
          highlight.style.fontFamily = "Montserrat-Bold, sans-serif";
        }
        
      }
    }
  }

  else {
    var time_ids = $('#schedule_view tr td').map(function(i,n) {
    return $(n).attr('id');
    }).get();

    var y;
    for (y = 0; y < time_ids.length; ++y) {
      var time = time_ids[y];
      var highlight = document.getElementById(time);
      highlight.style.backgroundColor = "#e2e2e2";
      highlight.style.fontFamily = "Montserrat-Light, sans-serif";
    }
  }
}

$(document).ready(function() {

  var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];

  var now = new Date();
  var day = days[ now.getDay() ];
  var date = now.getDate();
  var month = months[ now.getMonth() ];
  var year = now.getFullYear();

  var day_div = document.getElementById("day");
  day_div.innerHTML = day.toUpperCase();

  var date_div = document.getElementById("date");
  date_div.innerHTML = "- " + month + " " + date + " " + year + " -";

  $("#button_left").click(function() {  
    var cur = date_div.innerHTML.split(" ");
    var d = new Date(cur[3], months.indexOf(cur[1]), cur[2]);
    d.setDate(d.getDate() - 1);

    var day = days[ d.getDay() ];
    var date = d.getDate();
    var month = months[ d.getMonth() ];
    var year = d.getFullYear();

    day_div.innerHTML = day.toUpperCase();
    date_div.innerHTML = "- " + month + " " + date + " " + year + " -";
    if(d.getDay() != 0 && d.getDay() != 6)  
        updateScheduleInfo(d.getDay() - 1, THEarray[d.getDay() - 1]);
      else
          wipeDeBoard();
  });

  $("#button_right").click(function() {  
    var cur = date_div.innerHTML.split(" ");
    var d = new Date(cur[3], months.indexOf(cur[1]), cur[2]);
    d.setDate(d.getDate() + 1);

    var day = days[ d.getDay() ];
    var date = d.getDate();
    var month = months[ d.getMonth() ];
    var year = d.getFullYear();

    day_div.innerHTML = day.toUpperCase();
    date_div.innerHTML = "- " + month + " " + date + " " + year + " -";
    
    if(d.getDay() != 0 && d.getDay() != 6) 
        updateScheduleInfo(d.getDay() - 1, THEarray[d.getDay() - 1]);
      else
          wipeDeBoard();
  });

  $("#update").click(function() {  
    var liIds = $('#friends_added li').map(function(i,n) {
    return $(n).attr('id');
    }).get().join(',');

    console.log(initiateCompare(liIds));
  });
    
    
});