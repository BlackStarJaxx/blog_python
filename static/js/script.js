function loadComments() {
    $("#preloader").removeClass("d-none")
    $("#comments").html(" ")

    var post_id = $("input#post-id").attr("name")
    var url = "/api/article/posts/" + post_id + "/comments/";

    jQuery.ajax({
        url: url,
        type: "GET",
        success: function (data) {
            console.log(data)
            let html = " "
            data.forEach(comment => {
                html += "<div id=\"add-comment\" class=\"\">\n" +
                    "                                <hr>\n" +
                    "                                <h4><span class=\"text-info\">Author comment:</span> " + comment['author_comment'] + "</h4>\n" +
                    "                                <p><span class=\"text-info\">Message:</span>" + comment['body'] + "</p>\n" +
                    "                            </div>"

            })
            $("#comments").html("<h2>Comments</h2>" + html)
            $("#preloader").addClass("d-none")
        },
        error: function (e) {
            console.log(e)
        }
    });
}

function hideComments() {
    let show_comment = $("#show_comment_all");
    $("#send-form")[0].reset()


    if (show_comment.hasClass("d-none")) {
        $("#show-comment").html("Hide Comment");
        show_comment.removeClass("d-none");
    } else {
        $("#show-comment").html("Add Comment");
        show_comment.addClass("d-none")

    }
}

$(document).ready(() => {
    loadComments()
    $("form#send-form").submit(function (e) {
        e.preventDefault();
        var post_id = $("input#post-id").attr("name")
        var body = $("textarea#comment-body").val();
        var author = $("input#comment-author").val();
        var url = "/api/article/posts/" + post_id + "/comments/";
        //var url = "http://127.0.0.1:8001/api/article/posts/" + post_id + "/comments/";
        //var url = "http://127.0.0.1:8001/" + post_id + "/comments/";

        var data = {
            "body": body,
            "author_comment": author
        }

        jQuery.ajax({
            url: url,
            type: "POST",
            data: JSON.stringify(data),
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function (object) {
                loadComments()
                hideComments()
                $("#comment-added").removeClass("d-none")
                setTimeout(() => {
                    $("#comment-added").addClass("d-none")
                }, 3000);
            },
            errors: function (e) {
                console.log(e)
            }
        });
    });

    $("#like").click(function (e) {
        var post_id = $("input#post-id").attr("name")
        var url = "/api/article/posts/" + post_id + "/like/";
        //var url = "http://127.0.0.1:8001/api/article/posts/" + post_id + "/like/";
        //var url = "http://127.0.0.1:8001/" + post_id + "/like/";
        jQuery.ajax({
            url: url,
            type: "POST",
            success: function (object, status) {
                $("#like").text("Like " + object['likes'])
                let btn = $("#like")
                if (object['status'] == 'liked') {
                    btn.removeClass("btn-primary")
                    btn.removeClass("btn-danger")
                    btn.addClass("btn-success")
                } else {
                    btn.addClass("btn-danger")
                    btn.removeClass("btn-success")
                }
            },
            errors: function (e) {
                console.log(e)
            }
        });
    });

    $("#show-comment").click(function (e) {
        e.preventDefault()
        hideComments()
    });

});