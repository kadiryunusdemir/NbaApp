function search() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    page = document.getElementsByClassName('display-4')[0]

    if(page.innerHTML=='Player Attributes') {
        let x = document.getElementsByClassName('col-md-4 p-3 border bg-light');
      
        for (i = 0; i < x.length; i++) {
            var name = x[i].getElementsByClassName('name')[0].innerHTML.toLowerCase()
            var country = x[i].getElementsByClassName('country')[0].innerHTML.toLowerCase()
            var last_affilation = x[i].getElementsByClassName('last-affilation')[0].innerHTML.toLowerCase()
            var height = x[i].getElementsByClassName('height')[0].innerHTML.toLowerCase()
            var weight = x[i].getElementsByClassName('weight')[0].innerHTML.toLowerCase()
            var season_experience = x[i].getElementsByClassName('season-experience')[0].innerHTML.toLowerCase()
            var position = x[i].getElementsByClassName('position')[0].innerHTML.toLowerCase()
            var team = x[i].getElementsByClassName('team')[0].innerHTML.toLowerCase()
            if (name.includes(input) || country.includes(input) || last_affilation.includes(input) || height.includes(input) || weight.includes(input) || season_experience.includes(input) || position.includes(input) || team.includes(input)) {
                x[i].style.display="";  
            }
            else {
                x[i].style.display="none";                 
            }
        }
    }
    else if (page.innerHTML=='Players'){
        let x = document.getElementsByClassName('col-md-4 p-3 box-shadow');
      
        for (i = 0; i < x.length; i++) {
            var name = x[i].getElementsByClassName('btn btn-secondary')[0].innerHTML.toLowerCase()
            var first_name = x[i].getElementsByClassName('player-name')[0].innerHTML.toLowerCase()
            var id = x[i].getElementsByClassName('player-id')[0].innerHTML.toLowerCase()
            var last_name = x[i].getElementsByClassName('player-lastname')[0].innerHTML.toLowerCase()
            var is_active = x[i].getElementsByClassName('player-is-active')[0].innerHTML.toLowerCase()
            if (name.includes(input)  || first_name.includes(input) || last_name.includes(input) || id.includes(input) || is_active.includes(input)) {
                x[i].style.display="";  
            }
            else {
                x[i].style.display="none";                 
            }
        }
    }

    else if (page.innerHTML=='Player Photos'){
        let x = document.getElementsByClassName('card shadow-sm');
      
        for (i = 0; i < x.length; i++) {
            var name = x[i].getElementsByClassName('btn btn-light')[0].innerHTML.toLowerCase()
            if (name.includes(input)) {
                x[i].style.display="";  
            }
            else {
                x[i].style.display="none";                 
            }
        }
    }

    else if (page.innerHTML=='Player Bios'){
        let x = document.getElementsByClassName('col-md-4 p-3 border bg-light');
      
        for (i = 0; i < x.length; i++) {
            var name = x[i].getElementsByClassName('player-bio-name')[0].innerHTML.toLowerCase()
            var player_bio_bio = x[i].getElementsByClassName('player-bio-bio')[0].innerHTML.toLowerCase()
            var player_bio_table_name = x[i].getElementsByClassName('player-bio-table-name')[0].innerHTML.toLowerCase()
            var player_bio_player_image = x[i].getElementsByClassName('player-bio-player-image')[0].innerHTML.toLowerCase()
            var player_bio_player_slug = x[i].getElementsByClassName('player-bio-player-slug')[0].innerHTML.toLowerCase()
            var player_bio_transaction = x[i].getElementsByClassName('player-bio-transaction')[0].innerHTML.toLowerCase()
            var player_bio_date = x[i].getElementsByClassName('player-bio-date')[0].innerHTML.toLowerCase()
            var player_bio_description = x[i].getElementsByClassName('player-bio-description')[0].innerHTML.toLowerCase()
            var player_bio_slug = x[i].getElementsByClassName('player-bio-slug')[0].innerHTML.toLowerCase()
            var player_bio_team = x[i].getElementsByClassName('player-bio-team')[0].innerHTML.toLowerCase()
            var player_bio_slug_league = x[i].getElementsByClassName('player-bio-slug-league')[0].innerHTML.toLowerCase()
            var player_bio_salary = x[i].getElementsByClassName('player-bio-salary')[0].innerHTML.toLowerCase()
            var player_bio_contract = x[i].getElementsByClassName('player-bio-contract')[0].innerHTML.toLowerCase()
            var player_bio_position = x[i].getElementsByClassName('player-bio-position')[0].innerHTML.toLowerCase()
            var player_bio_height = x[i].getElementsByClassName('player-bio-height')[0].innerHTML.toLowerCase()
            var player_bio_weight = x[i].getElementsByClassName('player-bio-weight')[0].innerHTML.toLowerCase()
            var player_bio_birthdate = x[i].getElementsByClassName('player-bio-birthdate')[0].innerHTML.toLowerCase()
            var player_bio_birthplace = x[i].getElementsByClassName('player-bio-birthplace')[0].innerHTML.toLowerCase()
            if (name.includes(input) || player_bio_bio.includes(input) || player_bio_table_name.includes(input) || player_bio_birthplace.includes(input) || player_bio_player_image.includes(input)
                || player_bio_player_slug.includes(input) || player_bio_transaction.includes(input) || player_bio_date.includes(input) || player_bio_description.includes(input) || player_bio_slug.includes(input)
                || player_bio_team.includes(input) || player_bio_slug_league.includes(input) || player_bio_salary.includes(input) || player_bio_contract.includes(input)
                || player_bio_position.includes(input) || player_bio_height.includes(input) || player_bio_weight.includes(input) || player_bio_birthdate.includes(input)
            ) {
                x[i].style.display="";  
            }
            else {
                x[i].style.display="none";                 
            }
        }
    }

    else if (page.innerHTML=='Draft'){
        let x = document.getElementsByClassName('draft_tr');
      
        for (i = 0; i < x.length; i++) {
            var draft_year = x[i].getElementsByClassName('draft_year')[0].innerHTML.toLowerCase()
            var draft_number = x[i].getElementsByClassName('draft_number')[0].innerHTML.toLowerCase()
            var draft_number_round = x[i].getElementsByClassName('draft_number_round')[0].innerHTML.toLowerCase()
            var draft_number_round_pick = x[i].getElementsByClassName('draft_number_round_pick')[0].innerHTML.toLowerCase()
            var draft_name_organization = x[i].getElementsByClassName('draft_name_organization')[0].innerHTML.toLowerCase()
            var draft_type_organization = x[i].getElementsByClassName('draft_type_organization')[0].innerHTML.toLowerCase()
            var draft_id_player = x[i].getElementsByClassName('draft_id_player')[0].innerHTML.toLowerCase()
            var draft_id_team = x[i].getElementsByClassName('draft_id_team')[0].innerHTML.toLowerCase()
            var draft_profile_flag = x[i].getElementsByClassName('draft_profile_flag')[0].innerHTML.toLowerCase()
            var draft_slug_organization = x[i].getElementsByClassName('draft_slug_organization')[0].innerHTML.toLowerCase()
            var draft_location_organization = x[i].getElementsByClassName('draft_location_organization')[0].innerHTML.toLowerCase()

            if (
                draft_year.includes(input) || draft_number.includes(input) || draft_number_round.includes(input) || draft_slug_organization.includes(input) || draft_location_organization.includes(input)
                || draft_number_round_pick.includes(input) || draft_profile_flag.includes(input) || draft_id_team.includes(input) || draft_id_player.includes(input)
                || draft_name_organization.includes(input) || draft_type_organization.includes(input) 
            ) {
                x[i].style.display="";  
            }
            else {
                x[i].style.display="none";                 
            }
        }
    }

    else if (page.innerHTML=='Draft Combine'){
        let x = document.getElementsByClassName('draft_combine_tr');
      
        for (i = 0; i < x.length; i++) {
            var draft_combine_yearCombine = x[i].getElementsByClassName('draft_combine_yearCombine')[0].innerHTML.toLowerCase()
            var draft_combine_player_id = x[i].getElementsByClassName('draft_combine_player_id')[0].innerHTML.toLowerCase()
            var draft_combine_slugPosition = x[i].getElementsByClassName('draft_combine_slugPosition')[0].innerHTML.toLowerCase()
            var draft_combine_heightWOShoesInches = x[i].getElementsByClassName('draft_combine_heightWOShoesInches')[0].innerHTML.toLowerCase()
            var draft_combine_heightWOShoes = x[i].getElementsByClassName('draft_combine_heightWOShoes')[0].innerHTML.toLowerCase()
            var draft_combine_weightLBS = x[i].getElementsByClassName('draft_combine_weightLBS')[0].innerHTML.toLowerCase()
            var draft_combine_wingspanInches = x[i].getElementsByClassName('draft_combine_wingspanInches')[0].innerHTML.toLowerCase()
            var draft_combine_wingspan = x[i].getElementsByClassName('draft_combine_wingspan')[0].innerHTML.toLowerCase()
            var draft_combine_reachStandingInches = x[i].getElementsByClassName('draft_combine_reachStandingInches')[0].innerHTML.toLowerCase()
            var draft_combine_reachStandingO = x[i].getElementsByClassName('draft_combine_reachStandingO')[0].innerHTML.toLowerCase()
            var draft_combine_verticalLeapStandingInches = x[i].getElementsByClassName('draft_combine_verticalLeapStandingInches')[0].innerHTML.toLowerCase()
            var draft_combine_verticalLeapMaxInches = x[i].getElementsByClassName('draft_combine_verticalLeapMaxInches')[0].innerHTML.toLowerCase()
            var draft_combine_timeLane = x[i].getElementsByClassName('draft_combine_timeLane')[0].innerHTML.toLowerCase()
            var draft_combine_timeThree = x[i].getElementsByClassName('draft_combine_timeThree')[0].innerHTML.toLowerCase()
            var draft_combine_repsBench = x[i].getElementsByClassName('draft_combine_repsBench')[0].innerHTML.toLowerCase()

            if (
                draft_combine_repsBench.includes(input) || draft_combine_timeThree.includes(input) || draft_combine_timeLane.includes(input) || draft_combine_verticalLeapMaxInches.includes(input)
                || draft_combine_verticalLeapStandingInches.includes(input) || draft_combine_reachStandingO.includes(input) || draft_combine_reachStandingInches.includes(input)
                || draft_combine_wingspan.includes(input) || draft_combine_wingspanInches.includes(input) || draft_combine_weightLBS.includes(input) || draft_combine_heightWOShoes.includes(input)
                || draft_combine_heightWOShoesInches.includes(input) || draft_combine_slugPosition.includes(input) || draft_combine_player_id.includes(input) || draft_combine_yearCombine.includes(input)
            ) {
                x[i].style.display="";  
            }
            else {
                x[i].style.display="none";                 
            }
        }
    }

}