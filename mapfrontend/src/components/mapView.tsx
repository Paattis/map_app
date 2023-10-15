import React, { useState } from "react";
import { UserPoint } from "../classes/userpoint";

import { fromLonLat, toLonLat } from "ol/proj";
import { Point } from "ol/geom";
import "ol/ol.css";

import {
  RMap,
  ROSM,
  RLayerVector,
  RFeature,
  ROverlay,
  RStyle,
  RInteraction,
} from "rlayers";
import { User } from "../classes/user";
import NewUserPointForm from "./newUserPointForm";
//import locationIcon from "./svg/location.svg";

export interface IMapViewProps {
  userPoints: Array<UserPoint>;
  user: User | null;
}

export default function MapView(props: IMapViewProps) {
  const [newUserPoint, setNewUserPoint] = useState<UserPoint>();

  return (
    <div>
      <RMap
        className="example-map"
        width={"100%"}
        height={"500px"}
        initial={{
          center: fromLonLat([24.94030214683831, 60.1712000939996]),
          zoom: 10,
        }}
        onClick={(e) => {
          if (props.user) {
            const coords = toLonLat(e.map.getCoordinateFromPixel(e.pixel));

            let newUserPoint = {
              id: -1,
              label_text: "foo",
              user: { id: props.user.id, username: props.user.username },
              position: {
                type: "Point",
                coordinates: coords,
              },
            };

            setNewUserPoint(newUserPoint);
            console.log("newPoint");
          }
        }}
      >
        <ROSM />
        <RLayerVector zIndex={10}>
          <RStyle.RStyle></RStyle.RStyle>
          {props.userPoints.map((point) => (
            <RFeature
              key={point.id}
              geometry={new Point(fromLonLat(point.position.coordinates))}
            >
              <ROverlay className="example-overlay">
                {point.label_text}
              </ROverlay>
              {/* {<RInteraction.RDraw type={"Point"} />} */}
            </RFeature>
          ))}
        </RLayerVector>
      </RMap>
      {newUserPoint ? (
        <NewUserPointForm userPoint={newUserPoint}></NewUserPointForm>
      ) : (
        "Select a point"
      )}
    </div>
  );
}
