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

/*
{u'site_name': u'The Times of India', 
u'description': u'All-party delegation led by Home Minister Rajnath Singh will visit Jammu & Kashmir on September 4.\ 
                  The Home Minister had reviewed the situation in the valley with top BJP and government functionaries on Sunday.', 
u'title': u'Kashmir unrest: Rajnath to lead all-party delegation to Srinagar on September 4 - Times of India', 
u'url': u'http://timesofindia.indiatimes.com/india/Kashmir-unrest-Rajnath-to-lead-all-party-delegation-to-Srinagar-on-September-4/articleshow/53908155.cms', 
u'image': u'http://timesofindia.indiatimes.com/photo/53908150.cms', u'type': u'article'}
*/
// Script
var threshold=0;
$(document).ready(function() {
    $(document).endlessScroll({
        inflowPixels: 300,
        callback: function() {
              res={ "site_name": "The Times of India", 
                    "description": "", 
                    "title": "US Secretary of State John Kerry stuck in Delhi traffic, thanks to rain - Times of India", 
                    "url": "http://timesofindia.indiatimes.com/india/John-Kerry-stuck-in-Delhi-traffic-thanks-to-rain/articleshow/53915256.cms", 
                    "image": "http://timesofindia.indiatimes.com/photo/53915257.cms", 
                    "type": "article"
                  }
              
             if(threshold < 100000000){
                //var $img = $('#images li:nth-last-child(2)').clone();
                var loadable_content="<div id='post-content' class='w3-container'>\
                                          <!-- Multimedia content -->\
                                          <p>Testing the technique</p>\
                                          <!-- Text content -->\
                                          <div>\
                                              <a href='#' style='display:block;text-decoration:none !important;'\
                                                  onClick=\"window.open('"+res['url']+"', '_blank')\">\
                                                  <img src='"+res['image']+"' alt='' />\
                                                  <h4>"+res['title']+"</h4>\
                                                  <p>"+res['description']+"</p>\
                                                  <h5>"+res['site_name']+"</h5>\
                                              </a>\
                                          </div>\
                                          <div id='post-comments'>\
                                          <!-- post comments section-->\
                                          </div>\
                                      </div>"
                //alert(loadable_content)
                $('#post-background').html(loadable_content)
                var $img = $('#outer_wrap').clone();
                $('#repeated_content').append($img);
                threshold ++ ;}
        }
    });
});