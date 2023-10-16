class values {
  API_URL =
    process.env.NODE_ENV == "production"
      ? "api"
      : process.env.REACT_APP_DJANGO_URL;
}

export default new values();
