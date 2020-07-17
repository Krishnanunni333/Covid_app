mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless=true\n\
port=$PORT\n\
enable CORS = false\n\
\n\
">~/.streamlit/config.toml
