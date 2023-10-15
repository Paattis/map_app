import values from "../classes/values";

class AuthService {
  // TODO: get API URL from .env
  API_URL = values.API_URL;
  async login(username: string, password: string) {
    console.log(process.env);
    let url = `${this.API_URL}/token/`;
    console.log("Url", url);
    return fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: username, password: password }),
    })
      .then((r) => r.json())
      .then((data) => {
        if (!data.access) {
          throw data;
        }
        localStorage.setItem("token", JSON.stringify(data));
        return data;
      });
    //.catch((err) => console.log("err", err));
  }

  logOut() {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
  }
}

export default new AuthService();
