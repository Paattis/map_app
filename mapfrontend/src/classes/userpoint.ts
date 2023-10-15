import { Position } from "./position";
import { UserNoEmail } from "./user";

export type UserPoint = {
  id?: number;
  label_text: string;
  position: Position;
  user: UserNoEmail;
};
