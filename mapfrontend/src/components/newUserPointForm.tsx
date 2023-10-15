import * as React from "react";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Alert from "@mui/material/Alert";

import authService from "../services/auth.service";
import { UserPoint } from "../classes/userpoint";
import UserPointService from "../services/userpoint.service";
import { useState } from "react";
import "ol/ol.css";

export interface INewUserPointFormProps {
  userPoint: UserPoint;
  updateNewUserPoint: Function;
}

export default function NewUserPointForm(props: INewUserPointFormProps) {
  const [userPoint, setUserPoint] = useState<UserPoint>(props.userPoint);
  const [labelText, setLabelText] = useState<string>("");

  const submitNewPoint = (userPoint: UserPoint) => {
    UserPointService.createUserPoint(userPoint)
      .then((r) => {
        console.log("Userpoint added!", r);

        // Confirms that the latest (i.e. temporary) userPoint has been saved
        props.updateNewUserPoint(r);
        setLabelText("");
      })
      .catch((err) => {
        console.log("Error when adding", err);
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
      <h1>Position at {userPoint.position.coordinates.join(" ")}</h1>
      <TextField
        label="Label for point"
        value={labelText}
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
          if (userPoint) {
            submitNewPoint(userPoint);
          }
        }}
      >
        Save
      </Button>
    </>
  );
}
