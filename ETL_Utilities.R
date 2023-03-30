## ETL_Utilities.R
## An R utility package with ETL methods that may be useful. 


# NameTransform() ---------------------------------------------------------
# Utility to transform strings with special characters commonly found in names.
# Can easily be expanded / modified as needed.

library('stringr')

NameTransform <- function(name) {
    return(
        name %>%
        str_replace_all('Á|À|Â|Ä|Ã|Å','A') %>%
        str_replace_all('Æ','AE') %>%
        str_replace_all('ß','B') %>%
        str_replace_all('Ç','C') %>%
        str_replace_all('É|È|Ê|Ë','E') %>%
        str_replace_all('Í|Ì|Î|Ï','I') %>%
        str_replace_all('Ñ','N') %>%
        str_replace_all('Ó|Ò|Ô|Ö|Õ|Ø','O') %>%
        str_replace_all('Œ','OE') %>%
        str_replace_all('Ú|Ù|Û|Ü','U') %>%
        str_replace_all('á|à|â|ä|ã|å','a') %>%
        str_replace_all('æ','ae') %>%
        str_replace_all('ç','c') %>%
        str_replace_all('é|è|ê|ë','e') %>%
        str_replace_all('í|ì|î|ï','i') %>%
        str_replace_all('ñ','n') %>%
        str_replace_all('ó|ò|ô|ö|õ|ø','o') %>%
        str_replace_all('œ','oe') %>%
        str_replace_all('ú|ù|û|ü','u')
    )
}
