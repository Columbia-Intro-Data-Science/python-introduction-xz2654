library(readr)
movies <- read_csv("C:/Users/xz2654/Downloads/Selectedmoviesdata_10M.csv")

head(movies$title, 15)

for (i in 1:nrow(movies)){
  movies$title[i] <-  gsub(" \\(.*\\)", "", movies$title[i])
  if (endsWith(movies$title[i], 'The')){
    movies$title[i] <- paste('The', substr(movies$title[i], start = 1, stop = nchar(movies$title[i])-5))
  }
}

head(movies$title, 15)

write.csv(movies, file = "CleanedMovies10M.csv", row.names=FALSE)
