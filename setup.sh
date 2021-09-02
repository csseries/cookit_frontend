mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"michael.weitnauer@gmail.com\"\n\
" >> ~/.streamlit/credentials.toml

echo "\
[server]\n\
maxUploadSize = 10\n\
headless = true\n\
port = $PORT\n\
" >> ~/.streamlit/config.toml
