# The Food Atlas – Analyst workflow (base R, no packages needed)
# Run from the repository root:  source("analysis/analyst.R")   or   Rscript analysis/analyst.R
# Inputs : data/fpn_countries.csv, data/fpn_aggregates.csv (cleaned by scripts/clean_fpn.py and merge_all.py)
# Outputs: analysis/output/*.csv, and a check that every headline number in the report is reproduced.

countries  <- read.csv("data/fpn_countries.csv",  stringsAsFactors = FALSE)
aggregates <- read.csv("data/fpn_aggregates.csv", stringsAsFactors = FALSE)
out <- "analysis/output"
dir.create(out, showWarnings = FALSE, recursive = TRUE)
save <- function(x, name) write.csv(x, file.path(out, name), row.names = FALSE, na = "")

# ---- 1. Structure checks -------------------------------------------------------------
stopifnot(nrow(countries) == 1620, length(unique(countries$iso3)) == 180,
          !any(duplicated(countries[c("iso3", "year")])), nrow(aggregates) == 108)
for (v in c("CoHD_headcount", "pou", "stunting_pct")) {
  x <- countries[[v]]; stopifnot(all(is.na(x) | (x >= 0 & x <= 100)))
}

# ---- 2. Coverage by year (non-missing countries per indicator) -----------------------
cov_vars <- c("CoHD_PPP", "CoHD_headcount", "CoHD_unafford_n", "gdp_pc_ppp", "pou", "stunting_pct")
coverage <- do.call(rbind, lapply(sort(unique(countries$year)), function(y) {
  d <- countries[countries$year == y, ]
  data.frame(year = y, t(sapply(cov_vars, function(v) sum(!is.na(d[[v]])))))
}))
save(coverage, "coverage.csv")

# ---- 3. World trend 2017–2025 (official population-weighted aggregate) --------------
world <- aggregates[aggregates$iso3 == "WLD", c("year", "CoHD_PPP_PoP", "CoHD_headcount", "CoHD_unafford_n")]
world <- world[order(world$year), ]
save(world, "world_trend.csv")

# ---- 4. Regional and income-group change, 2017 to 2025 -------------------------------
a17 <- aggregates[aggregates$year == 2017, ]; a25 <- aggregates[aggregates$year == 2025, ]
agg <- merge(a17[c("iso3", "country", "group_type", "CoHD_headcount", "CoHD_unafford_n", "CoHD_PPP_PoP")],
             a25[c("iso3", "CoHD_headcount", "CoHD_unafford_n", "CoHD_PPP_PoP")], by = "iso3", suffixes = c("_2017", "_2025"))
agg$change_rate_pp      <- round(agg$CoHD_headcount_2025 - agg$CoHD_headcount_2017, 1)
agg$change_people_mn    <- round(agg$CoHD_unafford_n_2025 - agg$CoHD_unafford_n_2017, 1)
agg$share_of_world_2017 <- round(agg$CoHD_unafford_n_2017 / agg$CoHD_unafford_n_2017[agg$iso3 == "WLD"] * 100, 1)
agg$share_of_world_2025 <- round(agg$CoHD_unafford_n_2025 / agg$CoHD_unafford_n_2025[agg$iso3 == "WLD"] * 100, 1)
save(agg[order(agg$group_type, -agg$CoHD_headcount_2025), ], "aggregate_changes.csv")

# ---- 5. Countries, 2025, and change since 2017 ----------------------------------------
keep <- c("country", "iso3", "region", "income_group", "population", "gdp_pc_ppp", "CoHD_PPP", "CoHD_headcount", "CoHD_unafford_n")
c25 <- countries[countries$year == 2025, keep]
save(c25[order(-c25$CoHD_headcount, na.last = TRUE), ], "countries_2025.csv")
c17 <- countries[countries$year == 2017, c("iso3", "CoHD_PPP", "CoHD_headcount", "CoHD_unafford_n")]
chg <- merge(c25[c("country", "iso3", "region", "income_group", "CoHD_PPP", "CoHD_headcount", "CoHD_unafford_n")], c17,
             by = "iso3", suffixes = c("_2025", "_2017"))
chg$change_rate_pp   <- round(chg$CoHD_headcount_2025 - chg$CoHD_headcount_2017, 1)
chg$change_cost_pct  <- round((chg$CoHD_PPP_2025 / chg$CoHD_PPP_2017 - 1) * 100, 1)
save(chg[order(chg$country), ], "country_changes.csv")
rate <- c25[!is.na(c25$CoHD_headcount), ]
save(head(rate[order(-rate$CoHD_headcount), c("country", "iso3", "CoHD_headcount", "CoHD_unafford_n")], 10), "top10_rate_2025.csv")
save(head(rate[order(-rate$CoHD_unafford_n), c("country", "iso3", "CoHD_unafford_n", "CoHD_headcount")], 10), "top10_people_2025.csv")

# ---- 6. Income, price and affordability, 2025 (Spearman, unweighted, complete cases) --
spear <- function(x, y) cor(x, y, method = "spearman")
g <- c25[complete.cases(c25[c("gdp_pc_ppp", "CoHD_headcount")]), ]
p <- c25[complete.cases(c25[c("CoHD_PPP", "CoHD_headcount")]), ]
gp <- c25[complete.cases(c25[c("gdp_pc_ppp", "CoHD_PPP", "CoHD_headcount")]), ]
income_corr <- data.frame(
  pair = c("GDP per person vs share who cannot afford", "Diet cost vs share who cannot afford",
           "Diet cost vs share (GDP-complete sample)", "GDP per person vs diet cost (GDP-complete sample)"),
  n = c(nrow(g), nrow(p), nrow(gp), nrow(gp)),
  spearman_rho = round(c(spear(g$gdp_pc_ppp, g$CoHD_headcount), spear(p$CoHD_PPP, p$CoHD_headcount),
                         spear(gp$CoHD_PPP, gp$CoHD_headcount), spear(gp$gdp_pc_ppp, gp$CoHD_PPP)), 3))
save(income_corr, "income_correlations_2025.csv")

# ---- 7. Nutrition, 2024, and correlations 2022–2024 ----------------------------------
n24 <- countries[countries$year == 2024, c("country", "iso3", "region", "income_group", "population", "gdp_pc_ppp",
                                          "CoHD_headcount", "pou", "pou_below_2_5", "stunting_pct")]
save(n24[!is.na(n24$CoHD_headcount) & (!is.na(n24$pou) | !is.na(n24$stunting_pct)), ], "nutrition_2024.csv")
nc <- do.call(rbind, lapply(2022:2024, function(y) do.call(rbind, lapply(c("pou", "stunting_pct"), function(o) {
  d <- countries[countries$year == y & !is.na(countries$CoHD_headcount) & !is.na(countries[[o]]), ]
  data.frame(year = y, outcome = o, n = nrow(d),
             pearson_r = round(cor(d$CoHD_headcount, d[[o]]), 3), spearman_rho = round(spear(d$CoHD_headcount, d[[o]]), 3))
}))))
save(nc, "nutrition_correlations.csv")

# ---- 8. Sensitivity checks for the stunting association, 2024 ------------------------
s <- n24[!is.na(n24$CoHD_headcount) & !is.na(n24$stunting_pct), ]
sg <- s[!is.na(s$gdp_pc_ppp), ]
loo <- sapply(seq_len(nrow(s)), function(i) cor(s$CoHD_headcount[-i], s$stunting_pct[-i]))
res <- function(v) resid(lm(v ~ log(sg$gdp_pc_ppp)))
checks <- data.frame(
  check = c("Raw Pearson on GDP-complete matched sample", "Leave-one-country-out Pearson minimum",
            "Leave-one-country-out Pearson maximum", "Pearson residual correlation controlling log GDP per capita"),
  n = c(nrow(sg), nrow(s) - 1, nrow(s) - 1, nrow(sg)),
  value = round(c(cor(sg$CoHD_headcount, sg$stunting_pct), min(loo), max(loo),
                  cor(res(sg$CoHD_headcount), res(sg$stunting_pct))), 3))
for (grp in sort(unique(na.omit(s$income_group)))) {
  d <- s[!is.na(s$income_group) & s$income_group == grp, ]
  checks <- rbind(checks, data.frame(check = paste("Within income group Spearman:", grp), n = nrow(d),
                                     value = round(spear(d$CoHD_headcount, d$stunting_pct), 3)))
}
pu <- n24[!is.na(n24$CoHD_headcount) & !is.na(n24$pou) & !(n24$pou_below_2_5 %in% c(TRUE, "True")), ]
checks <- rbind(checks, data.frame(check = "PoU Spearman excluding censored <2.5 observations", n = nrow(pu),
                                   value = round(spear(pu$CoHD_headcount, pu$pou), 3)))
save(checks, "sensitivity_checks.csv")

# ---- 9. Headline numbers used in the report and the submission -----------------------
w <- function(y, v) world[world$year == y, v]
ssa <- agg[agg$iso3 == "SSF", ]
cty <- function(name, v) c25[c25$country == name, v]
ner <- n24[n24$iso3 == "NER", ]
headline <- data.frame(
  figure = c("World cost 2017", "World cost 2025", "World share 2017 (%)", "World share 2025 (%)", "World people 2025 (mn)",
             "SSA extra people 2017-2025 (mn)", "SSA share of world 2025 (%)", "Nigeria cost 2025", "Cyprus cost 2025",
             "Nigeria share 2025 (%)", "Cyprus share 2025 (%)", "Niger PoU 2024 (%)", "Niger share 2024 (%)", "Niger stunting 2024 (%)",
             "GDP vs share rho 2025", "Stunting vs share rho 2024", "Countries above 50% in 2025"),
  expected = c(2.94, 4.28, 41.0, 32.7, 2692.1, 194.3, 35.4, 4.18, 4.18, 80.5, 1.5, 12.9, 86.7, 48.3, -0.824, 0.784, 41),
  actual = c(w(2017, "CoHD_PPP_PoP"), w(2025, "CoHD_PPP_PoP"), w(2017, "CoHD_headcount"), w(2025, "CoHD_headcount"),
             w(2025, "CoHD_unafford_n"), ssa$change_people_mn, ssa$share_of_world_2025, cty("Nigeria", "CoHD_PPP"),
             cty("Cyprus", "CoHD_PPP"), cty("Nigeria", "CoHD_headcount"), cty("Cyprus", "CoHD_headcount"),
             ner$pou, ner$CoHD_headcount, ner$stunting_pct, round(income_corr$spearman_rho[1], 3),
             nc$spearman_rho[nc$year == 2024 & nc$outcome == "stunting_pct"], sum(rate$CoHD_headcount > 50)))
headline$ok <- abs(headline$actual - headline$expected) <= 0.051
save(headline, "headline_checks.csv")
print(headline, row.names = FALSE)
if (!all(headline$ok)) stop("Some headline numbers do not match the report – see analysis/output/headline_checks.csv")
cat("\nAll", nrow(headline), "headline numbers reproduced. Tables written to", out, "\n")
