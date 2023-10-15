import { TokenPair } from "../classes/tokenPair";
import values from "../classes/values";

class AuthService {
  // TODO: get API URL from .env
  API_URL = values.API_URL;
  async login(username: string, password: string) {
    console.log(process.env);
    let url = `${this.API_URL}/token/`;
    console.log("Url", url);
    const tokenPair: TokenPair = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: username, password: password }),
    }).then((r) => r.json());
    if (tokenPair.access) {
      localStorage.setItem("user", JSON.stringify(tokenPair));
    }
  }
}

export default new AuthService();
