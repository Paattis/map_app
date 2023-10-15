import React, { useEffect, useState } from "react";
import { UserPoint } from "../classes/userpoint";

import { fromLonLat, toLonLat } from "ol/proj";
import { Point, Polygon } from "ol/geom";
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
  const [tempUserPoint, setTempUserPoint] = useState<UserPoint>();
  const [userPoints, setUserPoints] = useState<Array<UserPoint>>(
    props.userPoints
  );

  useEffect(() => {
    setUserPoints(props.userPoints);
  }, [props.userPoints]);

  /**
   * Updates the temporary userpoint in the userPoints list in the state.
   * This updates the map
   */
  const updateNewUserPoint = (point: UserPoint) => {
    let lastUserPoint = userPoints[userPoints.length - 1];
    // only add a new unsaved marker on the map if we haven't done so already
    if (lastUserPoint.id != null) {
      userPoints.push(point);
    } else {
      // otherwise just replace the last unsaved one with the new one we made
      userPoints[userPoints.length - 1] = point;
    }
    setUserPoints(userPoints);
    setTempUserPoint(point);
    console.log("updateNewUserPoint called", point);
  };

  const getUserPointMarker = (point: UserPoint) => {
    if (!props.user || !point.user) {
      return "🔵";
    }
    return props.user.id == point.user.id ? "📍" : "🔵";
  };

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
            // convert the on-screen points to Lon/Lat coordinates
            const coords = toLonLat(e.map.getCoordinateFromPixel(e.pixel));

            // create a new temporary userPoint
            let newUserPoint = {
              label_text: "",
              user: { id: props.user.id, username: props.user.username },
              position: {
                type: "Point",
                coordinates: coords,
              },
            };

            setTempUserPoint(newUserPoint);
            updateNewUserPoint(newUserPoint);
          }
        }}
      >
        <ROSM />
        <RLayerVector zIndex={10}>
          {userPoints.map((point) => (
            <RFeature
              key={point.id || -1}
              geometry={new Point(fromLonLat(point.position.coordinates))}
            >
              <RStyle.RStyle>
                <RStyle.RStroke width={2} color={"yellow"} />
              </RStyle.RStyle>
              <ROverlay>
                {getUserPointMarker(point)}

                {point.label_text}
              </ROverlay>
            </RFeature>
          ))}
        </RLayerVector>
      </RMap>
      {tempUserPoint ? (
        <NewUserPointForm
          userPoint={tempUserPoint}
          updateNewUserPoint={updateNewUserPoint}
        ></NewUserPointForm>
      ) : (
        "Select a point"
      )}
    </div>
  );
}
