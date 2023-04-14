$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#rec_id").val(res.id);
        $("#rec_product_id").val(res.product_id);
        $("#rec_user_id").val(res.user_id);
        $("#rec_user_segment").val(res.user_segment);
        if (res.viewed_in_last7d == true) {
            $("#rec_viewed_in_last7d").val("true");
        } else {
            $("#rec_viewed_in_last7d").val("false");
        }
        if (res.bought_in_last30d == true) {
            $("#rec_bought_in_last30d").val("true");
        } else {
            $("#rec_bought_in_last30d").val("false");
        }
        $("#rec_last_relevance_date").val(res.last_relevance_date);
        if (res.recommendation_type == "SIMILAR_PRODUCT") {
            $("#rec_recommendation_type").val("SIMILAR_PRODUCT");
        } else if (res.recommendation_type == "RECOMMENDED_FOR_YOU") {
            $("#rec_recommendation_type").val("RECOMMENDED_FOR_YOU");
        }  else if (res.recommendation_type == "UPGRADE") {
            $("#rec_recommendation_type").val("UPGRADE");
        }  else if (res.recommendation_type == "FREQ_BOUGHT_TOGETHER") {
            $("#rec_recommendation_type").val("FREQ_BOUGHT_TOGETHER");
        }  else if (res.recommendation_type == "ADD_ON") {
            $("#rec_recommendation_type").val("ADD_ON");
        }  else if (res.recommendation_type == "TRENDING") {
            $("#rec_recommendation_type").val("TRENDING");
        }  else if (res.recommendation_type == "TOP_RATED") {
            $("#rec_recommendation_type").val("TOP_RATED");
        }  else if (res.recommendation_type == "NEW_ARRIVAL") {
            $("#rec_recommendation_type").val("NEW_ARRIVAL");
        } else {
            $("#rec_recommendation_type").val("UNKNOWN");
        }
        $("#rec_origin_product_id").val(res.origin_product_id);
        $("#rec_rating").val(res.rating);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#rec_id").val("");
        $("#rec_product_id").val("");
        $("#rec_user_id").val("");
        $("#rec_user_segment").val("");
        $("#rec_viewed_in_last7d").val("");
        $("#rec_bought_in_last30d").val("");
        $("#rec_last_relevance_date").val("");
        $("#rec_recommendation_type").val("");
        $("#rec_origin_product_id").val("");
        $("#rec_rating").val("UNKNOWN");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Recommendation
    // ****************************************

    $("#create-btn").click(function () {

        let id = $("#rec_id").val();
        let product_id = $("#rec_product_id").val();
        let user_id = $("#rec_user_id").val();
        let user_segment = $("#rec_user_segment").val();
        let viewed_in_last7d = $("#rec_viewed_in_last7d").val() == "true";
        let bought_in_last30d = $("#rec_bought_in_last30d").val() == "true";
        let last_relevance_date = $("#rec_last_relevance_date").val();
        let recommendation_type = $("#rec_recommendation_type").val();
        let origin_product_id = $("#rec_origin_product_id").val();
        let rating = $("#rec_rating").val();

        let data = {
            "id": id,
            "product_id": product_id,
            "user_id": user_id,
            "user_segment": user_segment,
            "viewed_in_last7d": viewed_in_last7d,
            "bought_in_last30d": bought_in_last30d,
            "last_relevance_date": last_relevance_date,
            "recommendation_type": recommendation_type,
            "origin_product_id": origin_product_id,
            "rating": rating
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/recommendations",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Recommendation
    // ****************************************

    $("#update-btn").click(function () {

        let id = $("#rec_id").val();
        let product_id = $("#rec_product_id").val();
        let user_id = $("#rec_user_id").val();
        let user_segment = $("#rec_user_segment").val();
        let viewed_in_last7d = $("#rec_viewed_in_last7d").val() == "true";
        let bought_in_last30d = $("#rec_bought_in_last30d").val() == "true";
        let last_relevance_date = $("#rec_last_relevance_date").val();
        let recommendation_type = $("#rec_recommendation_type").val();
        let origin_product_id = $("#rec_origin_product_id").val();
        let rating = $("#rec_rating").val();

        let data = {
            "id": id,
            "product_id": product_id,
            "user_id": user_id,
            "user_segment": user_segment,
            "viewed_in_last7d": viewed_in_last7d,
            "bought_in_last30d": bought_in_last30d,
            "last_relevance_date": last_relevance_date,
            "recommendation_type": recommendation_type,
            "origin_product_id": origin_product_id,
            "rating": rating
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/recommendations/${id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Recommendation
    // ****************************************

    $("#retrieve-btn").click(function () {

        let id = $("#rec_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/recommendations/${id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Recommendation
    // ****************************************

    $("#delete-btn").click(function () {

        let id = $("#rec_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/recommendations/${id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Recommendation has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#rec_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Recommendation
    // ****************************************

    $("#search-btn").click(function () {

        let product_id = $("#rec_product_id").val();
        let user_id = $("#rec_user_id").val();
        let user_segment = $("#rec_user_segment").val();
        let viewed_in_last7d = $("#rec_viewed_in_last7d").val() == "true";
        let bought_in_last30d = $("#rec_bought_in_last30d").val() == "true";

        let queryString = ""

        if (product_id) {
            queryString += 'product_id=' + product_id
        }
        if (user_id) {
            if (queryString.length > 0) {
                queryString += '&user_id=' + user_id
            } else {
                queryString += 'user_id=' + user_id
            }
        }
        if (user_segment) {
            if (queryString.length > 0) {
                queryString += '&user_segment=' + user_segment
            } else {
                queryString += 'user_segment=' + user_segment
            }
        }
        if (viewed_in_last7d) {
            if (queryString.length > 0) {
                queryString += '&viewed_in_last7d=' + viewed_in_last7d
            } else {
                queryString += 'viewed_in_last7d=' + viewed_in_last7d
            }
        }
        if (bought_in_last30d) {
            if (queryString.length > 0) {
                queryString += '&bought_in_last30d=' + bought_in_last30d
            } else {
                queryString += 'bought_in_last30d=' + bought_in_last30d
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/recommendations?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<h4>Search Results:</h4>'
            table += '<thead><tr>'
            table += '<th class="col-md-1"># ID</th>'
            table += '<th class="col-md-1">Product ID</th>'
            table += '<th class="col-md-1">User ID</th>'
            table += '<th class="col-md-2">User Segment</th>'
            table += '<th class="col-md-1">Viewed in Lst7d</th>'
            table += '<th class="col-md-1">Bought in Lst30d</th>'
            table += '<th class="col-md-1">Last Rlvnc. Date</th>'
            table += '<th class="col-md-2">Type</th>'
            table += '<th class="col-md-1">Org. Product ID</th>'
            table += '<th class="col-md-1">Rating</th>'
            table += '</tr></thead><tbody>'
            let firstRec = "";
            for(let i = 0; i < res.length; i++) {
                let rec = res[i];
                table +=  `<tr id="row_${i}"><td>${rec.id}</td><td>${rec.product_id}</td><td>${rec.user_id}</td><td>${rec.user_segment}</td><td>${rec.viewed_in_last7d}</td><td>${rec.bought_in_last30d}</td><td>${rec.last_relevance_date}</td><td>${rec.recommendation_type}</td><td>${rec.origin_product_id}</td><td>${rec.rating}</td></tr>`;
                if (i == 0) {
                    firstRec = rec;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstRec != "") {
                update_form_data(firstRec)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})

    // ****************************************
    // Rate a Recommendation
    // ****************************************

    $("#rate-btn").click(function () {

        let id = $("#rec_id").val();
        let rating = $("#rec_rating").val();

        let data = {
            "id": id,
            "rating": rating
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/recommendations/${id}/rate`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

