import * as React from "react";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Alert from "@mui/material/Alert";

import authService from "../services/auth.service";
import { UserPoint } from "../classes/userpoint";
import UserPointService from "../services/userpoint.service";
import { useState } from "react";
import "ol/ol.css";
import { User } from "../classes/user";

export interface INewUserPointFormProps {
  userPoint: UserPoint;
  updateNewUserPoint: Function;
  changeUserPoint: Function;
}

export default function NewUserPointForm(props: INewUserPointFormProps) {
  const [userPoint, setUserPoint] = useState<UserPoint>(props.userPoint);
  const [labelText, setLabelText] = useState<string>("");

  const submitNewUserPoint = (userPoint: UserPoint) => {
    UserPointService.createUserPoint(userPoint)
      .then((userPoint) => {
        console.log("Userpoint added!", userPoint);

        // Confirms that the latest (i.e. temporary) userPoint has been saved
        props.updateNewUserPoint(userPoint);
        setLabelText("");
      })
      .catch((err) => {
        console.log("Error when adding", err);
      });
  };

  const updateUserPoint = (userPoint: UserPoint) => {
    UserPointService.updateUserPoint(userPoint).then((userPoint) => {
      console.log("Userpoint updated!", userPoint);
      setLabelText("");
      setUserPoint(userPoint);
    });
  };

  React.useEffect(() => {
    console.log(
      "Userpoint change",
      props.userPoint,
      props.userPoint.label_text
    );
    setUserPoint(props.userPoint);
  }, [props.userPoint.position]);

  return (
    <>
      <h3>
        {userPoint.id ? "Editing" : "Adding a"} point at{" "}
        {userPoint.position.coordinates.join(", ")}
      </h3>
      <TextField
        label="Label for point"
        value={userPoint.label_text}
        onChange={(e) => {
          userPoint.label_text = e.target.value;
          setUserPoint(userPoint);
          setLabelText(userPoint.label_text);
          props.updateNewUserPoint(userPoint);
        }}
      ></TextField>
      <Button
        variant="contained"
        onClick={() => {
          if (!userPoint.id) {
            submitNewUserPoint(userPoint);
          } else {
            updateUserPoint(userPoint);
          }
        }}
      >
        Save
      </Button>
    </>
  );
}
