import delimited "../../Desktop/Work/TikTok_New/data/bot_data/political_regression_data.csv", clear

encode state, gen(state_id)
encode leaning_grouped, gen(leaning_id)

reghdfe is_mismatched b2i.leaning_id i.state_id top_account_democrat top_account_republican negative_democrat negative_republican persona_anti_rate num_videos_watched transcript_availability_rate engagement_score_persona likes_per_recommendation comments_per_recommendation opp_pro persona_count duration videocount followercount sharecount, vce(cluster week device)

parmest, saving(coeffs_raw, replace) norestore list(estimate stderr p parm)

use coeffs_raw.dta, clear

multproc, pvalue(p) method(bonferroni) gpcor(p_corrected)


list parm estimate p p_corrected stderr, sep(0)

export delimited parm estimate p p_corrected stderr using "../../Desktop/Work/TikTok_New/data/tables/full_regression_output_raw.csv", replace
