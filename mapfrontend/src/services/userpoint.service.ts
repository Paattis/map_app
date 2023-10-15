import values from "../classes/values";
import { UserPoint } from "../classes/userpoint";
import authService from "./auth.service";

class UserPointService {
  // TODO: get API URL from .env
  API_URL = values.API_URL;
  async fetchUserPoints(): Promise<Array<UserPoint>> {
    const data: Array<UserPoint> = await fetch(
      `${this.API_URL}/userpoints/`
    ).then((r) => {
      if (!r.ok) return [];
      return r.json();
    });
    return data;
  }

  /**
   * Sends a POST request to create a brand new UserPoint.
   *
   * @async
   * @param {UserPoint} userPoint
   * @returns {Promise<UserPoint>}
   */
  async createUserPoint(userPoint: UserPoint): Promise<UserPoint> {
    let token = await authService.getTokens();

    const data = await fetch(`${this.API_URL}/userpoints/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token?.access}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userPoint),
    }).then((r) => {
      if (!r.ok) throw r.json();
      return r.json();
    });
    return data;
  }

  /**
   * Sends a PUT request to update the UserPoint with fresh new data.   *
   * @async
   * @param {UserPoint} userPoint
   * @returns {Promise<UserPoint>}
   */
  async updateUserPoint(userPoint: UserPoint): Promise<UserPoint> {
    let token = await authService.getTokens();
    const data = await fetch(`${this.API_URL}/userpoints/${userPoint.id}/`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token?.access}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userPoint),
    }).then((r) => {
      if (!r.ok) throw r.json();
      return r.json();
    });
    return data;
  }
}

export default new UserPointService();
