'use strict';

(function ($) {
    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");

        /*------------------
            Portfolio filter
        --------------------*/
        $('.portfolio__filter li').on('click', function () {
            $('.portfolio__filter li').removeClass('active');
            $(this).addClass('active');
        });
        if ($('.portfolio__gallery').length > 0) {
            var containerEl = document.querySelector('.portfolio__gallery');
            var mixer = mixitup(containerEl);
        }
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Masonary
    //    $('.work__gallery').masonry({
    //        itemSelector: '.work__item',
    //        columnWidth: '.grid-sizer',
    //        gutter: 10
    //    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*------------------
		Hero Slider
	--------------------*/
    $('.hero__slider').owlCarousel({
        loop: true,
        dots: true,
        mouseDrag: false,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        items: 1,
        margin: 0,
        smartSpeed: 1200,
        autoplayTimeout: 5000,
        autoplayHoverPause: true,
        autoplay: true,
        autoHeight: false,
    });


    var dot = $('.hero__slider .owl-dot');
    dot.each(function () {
        var index = $(this).index() + 1;
        if (index < 10) {
            $(this).html('0').append(index);
        } else {
            $(this).html(index);
        }
    });

    /*------------------
        Testimonial Slider
    --------------------*/
    $(".testimonial__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 3,
        dots: true,
        dotsEach: 2,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {
            992: {
                items: 3
            },
            768: {
                items: 2
            },
            320: {
                items: 1
            }
        }
    });

    /*------------------
        Latest Slider
    --------------------*/
    $(".latest__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 3,
        dots: true,
        dotsEach: 2,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: false,
        responsive: {
            992: {
                items: 3
            },
            768: {
                items: 2
            },
            320: {
                items: 1
            }
        }
    });

    /*------------------
        Movies Slider
    --------------------*/
    $(".movie__carousel").owlCarousel({
        loop: true,
        margin: 20,         // smaller margin for better spacing
        items: 4,           // default number of items
        dots: true,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {
            0: {
                items: 2
            },
            480: {
                items: 3
            },
            768: {
                items: 4
            },
            992: {
                items: 5
            },
            1200: {
                items: 4
            }
        }
    });

    /*------------------
        Video Popup
    --------------------*/
    //    $('.video-popup').magnificPopup({
    //        type: 'iframe'
    //    });

    /*------------------
        Counter
    --------------------*/
    $('.counter_num').each(function () {
        $(this).prop('Counter', 0).animate({
            Counter: $(this).text()
        }, {
            duration: 4000,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now));
            }
        });
    });

    /*---------state-------------*/

    // When country is selected → load states
    //    $(".country-data").change(function () {
    //        const countryId = $(this).val();
    //
    //        $.ajax({
    //            url: ajaxUrls.loadStates,
    //            data: { country_id: countryId },
    //            success: function (data) {
    //                $(".state-data").html('<option value="">Select the state</option>');
    //
    //                data.forEach(function (state) {
    //                    $(".state-data").append(
    //                        `<option value="${state.id}">${state.name}</option>`
    //                    );
    //                });
    //            }
    //        });
    //    });





})(jQuery);


if(document.getElementById("country-select") !== null)
{
    document.getElementById("country-select").addEventListener("change", function () {
        const countryId = this.value;

        const stateSelect = document.getElementById("state-select");

        // Reset dropdown
        stateSelect.innerHTML = '<option value="">Select State</option>';

        if (countryId && locations[countryId]) {
            const states = locations[countryId]["states"];

            // Add states
            for (const stateId in states) {
                const option = document.createElement("option");
                option.value = stateId;
                option.text = states[stateId];   // state name
                stateSelect.appendChild(option);
            }
        }
    });

}



// for the time of theatre---------------------------------------------


const getSeeBtn = document.getElementById('see-password');
const getPassword = document.getElementById('password');
const eyeIcon = document.getElementById('eye-icon');

getSeeBtn.addEventListener('click', function () {
    if (getPassword.type === 'password') {
        getPassword.type = 'text';
        getPassword.style.backgroundColor = '#ffae6b';

        eyeIcon.classList.remove('fa-eye-slash');
        eyeIcon.classList.add('fa-eye');


    } else if(getPassword.type === 'text'){
        getPassword.type = 'password';
        getPassword.style.backgroundColor = '#ffffff';



        eyeIcon.classList.remove('fa-eye');
        eyeIcon.classList.add('fa-eye-slash');
    }
});

