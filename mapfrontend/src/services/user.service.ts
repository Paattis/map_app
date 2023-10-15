import values from "../classes/values";
import jwt_decode from "jwt-decode";
import { TokenPair } from "../classes/tokenPair";
import { TokenData } from "../classes/tokenData";
import { User } from "../classes/user";
import authService from "./auth.service";

class UserService {
  // TODO: get API URL from .env
  API_URL = values.API_URL;
  async fetchUserData(): Promise<User | null> {
    // decode jwt token to get user's id
    let tokenPair = await authService.getTokens();
    if (tokenPair != null) {
      console.log("Decoding token", tokenPair);
      let decodedToken: TokenData = jwt_decode(tokenPair.access);

      let url = `${this.API_URL}/users/${decodedToken.user_id}/`;

      return fetch(url, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${tokenPair.access}`,
        },
      }).then((r) => {
        if (!r.ok) return null;
        let data = r.json();
        console.log("Saving", data, "as user");
        localStorage.setItem("user", JSON.stringify(data));
        return data;
      });
    } else {
      return null;
    }
  }

  getUserData() {
    return JSON.parse(localStorage.getItem("user") || "{}");
  }
}

export default new UserService();
