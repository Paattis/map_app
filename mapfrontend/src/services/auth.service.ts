import { TokenPair } from "../classes/tokenPair";
import values from "../classes/values";

class AuthService {
  // TODO: get API URL from .env
  API_URL = values.API_URL;

  /**
   * Fetches access tokens in exchange for the correct login credentials.
   * @async
   * @param {string} username
   * @param {string} password
   * @returns {Promise<TokenPair>}
   */
  async login(username: string, password: string): Promise<TokenPair> {
    let url = `${this.API_URL}/token/`;

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
  }

  logOut() {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
  }

  /**
   * Gets the current JWT `TokenPair` from localStorage.
   * @returns {(TokenPair | null)}
   */
  getTokens(): TokenPair | null {
    if (localStorage.getItem("token")) {
      return JSON.parse(localStorage.getItem("token") || "{}") as TokenPair;
    }

    return null;
  }
}

export default new AuthService();
