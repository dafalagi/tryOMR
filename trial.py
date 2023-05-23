import tinify

tinify.key = "API_KEY"

source = tinify.from_file("4.jpeg")
source.to_file("4-optimized.jpeg")