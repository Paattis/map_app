import values from "../classes/values";
import { UserPoint } from "../classes/userpoint";

class UserPointService {
  // TODO: get API URL from .env
  API_URL = values.API_URL;
  async fetchUserPoints(): Promise<Array<UserPoint>> {
    const data: Array<UserPoint> = await fetch(
      `${this.API_URL}/userpoints/`,
      {}
    ).then((r) => {
      if (!r.ok) return [];
      return r.json();
    });
    return data;
  }
}

export default new UserPointService();
