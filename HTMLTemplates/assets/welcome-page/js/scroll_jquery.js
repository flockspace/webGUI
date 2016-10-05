/**
 * Endless Scroll plugin for jQuery
 *
 * v1.4.8
 *
 * Copyright (c) 2008 Fred Wu
 *
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 */

/**
 * Usage:
 *
 * // using default options
 * $(document).endlessScroll();
 *
 * // using some custom options
 * $(document).endlessScroll({
 *   fireOnce: false,
 *   fireDelay: false,
 *   loader: "<div class=\"loading\"><div>",
 *   callback: function(){
 *     alert("test");
 *   }
 * });
 *
 * Configuration options:
 *
 * bottomPixels  integer          the number of pixels from the bottom of the page that triggers the event
 * fireOnce      boolean          only fire once until the execution of the current event is completed
 * fireDelay     integer          delay the subsequent firing, in milliseconds, 0 or false to disable delay
 * loader        string           the HTML to be displayed during loading
 * data          string|function  plain HTML data, can be either a string or a function that returns a string,
 *                                when passed as a function it accepts one argument: fire sequence (the number
 *                                of times the event triggered during the current page session)
 * insertAfter   string           jQuery selector syntax: where to put the loader as well as the plain HTML data
 * callback      function         callback function, accepts one argument: fire sequence (the number of times
 *                                the event triggered during the current page session)
 * resetCounter  function         resets the fire sequence counter if the function returns true, this function
 *                                could also perform hook actions since it is applied at the start of the event
 * ceaseFire     function         stops the event (no more endless scrolling) if the function returns true
 *
 * Usage tips:
 *
 * The plugin is more useful when used with the callback function, which can then make AJAX calls to retrieve content.
 * The fire sequence argument (for the callback function) is useful for 'pagination'-like features.
 */

(function($){

  $.fn.endlessScroll = function(options) {

    var defaults = {
      bottomPixels: 50,
      fireOnce: true,
      fireDelay: 150,
      loader: "<br />Loading...<br />",
      data: "",
      insertAfter: "div:last",
      resetCounter: function() { return false; },
      callback: function() { return true; },
      ceaseFire: function() { return false; }
    };

    var options = $.extend({}, defaults, options);

    var firing       = true;
    var fired        = false;
    var fireSequence = 0;

    if (options.ceaseFire.apply(this) === true) {
      firing = false;
    }

    if (firing === true) {
      $(this).scroll(function() {
        if (options.ceaseFire.apply(this) === true) {
          firing = false;
          return; // Scroll will still get called, but nothing will happen
        }

        if (this == document || this == window) {
          var is_scrollable = $(document).height() - $(window).height() <= $(window).scrollTop() + options.bottomPixels;
        } else {
          // calculates the actual height of the scrolling container
          var inner_wrap = $(".endless_scroll_inner_wrap", this);
          if (inner_wrap.length == 0) {
            inner_wrap = $(this).wrapInner("<div class=\"endless_scroll_inner_wrap\" />").find(".endless_scroll_inner_wrap");
          }
          var is_scrollable = inner_wrap.length > 0 &&
            (inner_wrap.height() - $(this).height() <= $(this).scrollTop() + options.bottomPixels);
        }

        if (is_scrollable && (options.fireOnce == false || (options.fireOnce == true && fired != true))) {
          if (options.resetCounter.apply(this) === true) fireSequence = 0;

          //fired variable setting to true makes the scrolling halt. Hence it is set to false which seemless scrolling
          fired = false;
          fireSequence++;

          $(options.insertAfter).after("<div id=\"endless_scroll_loader\">" + options.loader + "</div>");

          data = typeof options.data == 'function' ? options.data.apply(this, [fireSequence]) : options.data;

          if (data !== false) {
            $(options.insertAfter).after("<div id=\"endless_scroll_data\">" + data + "</div>");
            $("div#endless_scroll_data").hide().fadeIn();
            $("div#endless_scroll_data").removeAttr("id");

            options.callback.apply(this, [fireSequence]);

            if (options.fireDelay !== false || options.fireDelay !== 0) {
              $("body").after("<div id=\"endless_scroll_marker\"></div>");
              // slight delay for preventing event firing twice
              $("div#endless_scroll_marker").fadeTo(options.fireDelay, 1, function() {
                $(this).remove();
                fired = false;
              });
            }
            else {
              fired = false;
            }
          }

          $("div#endless_scroll_loader").remove();
        }
      });
    }
  };

})(jQuery);

// 'csrfmiddlewaretoken':'sOF4XutrqZ8xj7p31GmXZq83F5wBTDp1wr8diBJZ8J3TSg5pTRRDv24rEHEEdtoy'


// Script
$(document).ready(function() {
    $(document).endlessScroll({
        inflowPixels: 300,
        callback: function() {
            
              $.ajax({
                      url:'http://127.0.0.1/fetch_post_content',
                      type:'GET', //GET request should not have CSRF token
                      //dataType:'JSON', Don't use dataType:JSON
                      //data:{'csrfmiddlewaretoken': 'sOF4XutrqZ8xj7p31GmXZq83F5wBTDp1wr8diBJZ8J3TSg5pTRRDv24rEHEEdtoy'},//'{{csrf_token}}'},
                      //data:{'csrfmiddlewaretoken':'{{csrf_token}}'}
                    }).success(function(successObj){ //fail and success function names are interchanged for experiment
                        //console.log("At success callback function")
                        //console.log(successObj);
                        response = successObj['posts']
                        console.log(response);
                        for (i = 0; i < response.length; i++) { 
                            obj = JSON.parse(response[i])
                            if (obj['content_type']=='image')
                              dynamic_load_imgContent(obj);
                            else if (obj['content_type']=='audio')
                              dynamic_load_audioContent(obj)
                            else if (obj['content_type']=='video')
                              dynamic_load_videoContent(obj)
                        }
                        
                    }).fail(function(failObj){
                        console.log("Endless scroll callback function failed!")
                        console.log(failObj);
                    });

              function dynamic_load_imgContent(obj){
                  imgContent = '<div class="row">'+
                                  '<div class="col s12 m7 ">'+
                                      '<div class="card hoverable">'+
                                          '<div class="card-image">'+
                                              '<img src="http://127.0.0.1/media/'+obj['content_location']+'">'+
                                                  '<span class="card-title">'+obj['content_title']+'</span>'+
                                          '</div>'+
                                          '<div class="card-content ">'+
                                              '<p>'+obj['content_description']+'</p>'+
                                          '</div>'+
                                          '<div class="card-action">'+
                                              'shared by <a href="#" >'+obj['user_fname']+' '+obj['user_lname']+'</a>'+
                                          '</div>'+
                                      '</div>'+
                                  '</div>'+
                                '</div>'

                  console.log(imgContent);
                  $('#contentCard').append(imgContent);
                  return;
              }

              function dynamic_load_audioContent(obj){
                  audioContent = '<div class="row">'+
                                  '<div class="col s12 m7 ">'+
                                      '<div class="card hoverable">'+
                                          '<div class="card-image">'+
                                              '<audio src="http://127.0.0.1/media/'+obj['content_location']+'" style="width:100%;" controls >'+
                                              '</audio>'+
                                          '</div>'+
                                          '<div class="card-content ">'+
                                              '<p>'+obj['content_description']+'</p>'+
                                          '</div>'+
                                          '<div class="card-action">'+
                                              'shared by <a href="#" >'+obj['user_fname']+' '+obj['user_lname']+'</a>'+
                                          '</div>'+
                                      '</div>'+
                                  '</div>'+
                                '</div>'
                  console.log(audioContent);
                  $('#contentCard').append(audioContent);
                  return;
              }

              function dynamic_load_videoContent(obj){
                  videoContent = '<div class="row">'+
                                  '<div class="col s12 m7 ">'+
                                      '<div class="card hoverable">'+
                                          '<div class="card-image">'+
                                              '<video src="http://127.0.0.1/media/'+obj['content_location']+'" style="width:100%;height:100%;" controls >'+
                                              '</video>'+    
                                          '</div>'+
                                          '<div class="card-content ">'+
                                              '<p>'+obj['content_description']+'</p>'+
                                          '</div>'+
                                          '<div class="card-action">'+
                                              'shared by <a href="#" >'+obj['user_fname']+' '+obj['user_lname']+'</a>'+
                                          '</div>'+
                                      '</div>'+
                                  '</div>'+
                                '</div>'
                  console.log(videoContent);
                  $('#contentCard').append(videoContent);
                  return;
              }

        }

    });
});