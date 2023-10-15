import jwtDecode from "jwt-decode";
import { TokenPair } from "../classes/tokenPair";
import values from "../classes/values";
import jwt_decode from "jwt-decode";
import { TokenData } from "../classes/tokenData";

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

  /**
   * Hits the `/token/refresh/` endpoint to fetch a new token pair.
   *
   * @async
   * @param {TokenPair} tokenPair
   * @returns {Promise<TokenPair>}
   */
  async refreshToken(tokenPair: TokenPair): Promise<TokenPair> {
    let url = `${this.API_URL}/token/refresh/`;
    console.log("TokenPair used", tokenPair);
    return fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh: tokenPair.refresh }),
    })
      .then((r) => r.json())
      .then((data) => {
        if (!data.access) {
          throw data;
        }
        // replace accessToken in token pair with new refresh token
        let tokenPair = this.getTokenFromStorage();
        if (tokenPair) {
          tokenPair.access = data.access;
        }

        localStorage.setItem("token", JSON.stringify(tokenPair));
        return data;
      });
  }

  decodeToken(token: string) {
    let decoded_token: TokenData = jwt_decode(token);
    return decoded_token;
  }

  parseToken(token: string): TokenPair {
    return JSON.parse(token);
  }

  logOut() {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
  }

  /**
   * Gets the token pair from localStorage and parses it
   *
   * @returns {TokenPair}
   */
  getTokenFromStorage(): TokenPair | null {
    let rawToken = localStorage.getItem("token");
    if (rawToken) {
      return this.parseToken(rawToken);
    }
    return null;
  }

  /**
   * Gets the current JWT `TokenPair` from localStorage and refreshes it if necessary.
   * @returns {(TokenPair | null)}
   */
  async getTokens(): Promise<TokenPair | null> {
    let tokenPair = this.getTokenFromStorage();

    if (tokenPair) {
      let decoded_access_token = this.decodeToken(tokenPair.access);

      // check if about to expire
      let currentTimeStamp = Math.round(Date.now() / 1000);
      let tokenExpireTime = decoded_access_token.exp;

      if (tokenExpireTime < currentTimeStamp) {
        let newPair: TokenPair = await this.refreshToken(tokenPair);
        console.log(tokenExpireTime, "<", currentTimeStamp);
        console.log("refreshing");
        return newPair;
      }

      return tokenPair;
    }

    return null;
  }
}

export default new AuthService();
