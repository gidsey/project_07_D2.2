$(document).ready(function () {

    $('textarea').autogrow({onInitialize: true});


    //Cloner for infinite input lists
    $(".circle--clone--list").on("click", ".circle--clone--add", function () {
        var parent = $(this).parent("li");
        var copy = parent.clone();
        parent.after(copy);
        copy.find("input, textarea, select").val("");
        copy.find("*:first-child").focus();
    });

    $(".circle--clone--list").on("click", "li:not(:only-child) .circle--clone--remove", function () {
        var parent = $(this).parent("li");
        parent.remove();
    });

    // Adds class to selected item
    $(".circle--pill--list a").click(function () {
        $(".circle--pill--list a").removeClass("selected");
        $(this).addClass("selected");
    });

    // Adds class to parent div of select menu
    $(".circle--select select").focus(function () {
        $(this).parent().addClass("focus");
    }).blur(function () {
        $(this).parent().removeClass("focus");
    });

    // Clickable table row
    $(".clickable-row").click(function () {
        var link = $(this).data("href");
        var target = $(this).data("target");

        if ($(this).attr("data-target")) {
            window.open(link, target);
        } else {
            window.open(link, "_self");
        }
    });

    // Custom File Inputs
    var input = $(".circle--input--file");
    var text = input.data("text");
    var state = input.data("state");
    input.wrap(function () {
        return "<a class='button " + state + "'>" + text + "</div>";
    });

    // Password Strength Meter for Change Password Page
    $('#id_new_password').password({
        field: "#name-check", // select the match field (selector or jQuery instance) for better password checks
        fieldPartialMatch: true,
        containsField: 'The password contains your name',
        minimumLength: 14 // minimum password length (below this threshold, the score is 0)
    });

    $('#id_new_password').on('password.score', (e, score) => {
        console.log('Called every time a new score is calculated (this means on every keyup)')
        console.log('Current score is %d', score)
    })

    $('#id_new_password').on('password.text', (e, text, score) => {
        console.log('Called every time the text is changed (less updated than password.score)')
        console.log('Current message is %s with a score of %d', text, score)
    })


    // Password Strength Meter Create Account Page
    $('#id_password1').password({
        field: false, // select the match field (selector or jQuery instance) for better password checks
        fieldPartialMatch: true,
        containsField: 'The password contains your name',
        minimumLength: 14 // minimum password length (below this threshold, the score is 0)
    });

    $('#id_password1').on('password.score', (e, score) => {
        console.log('Called every time a new score is calculated (this means on every keyup)')
        console.log('Current score is %d', score)
    })

    $('#id_password1').on('password.text', (e, text, score) => {
        console.log('Called every time the text is changed (less updated than password.score)')
        console.log('Current message is %s with a score of %d', text, score)
    })


    //  Datepicker
    $(function () {
        $("#id_date_of_birth").datepicker({
            format: 'YYYY-MM-DD',
        });
    });

    // Summernote (multiple editors)
    $(document).ready(function () {
        $('.summernote').summernote();
    });

});