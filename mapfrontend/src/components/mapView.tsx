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
import { RFill, RStroke } from "rlayers/style";
//import locationIcon from "./svg/location.svg";
import { Position } from "../classes/position";
import userpointService from "../services/userpoint.service";

export interface IMapViewProps {
  userPoints: Array<UserPoint>;
  user: User | null;
}

export default function MapView(props: IMapViewProps) {
  // the userPoint we are currently adding or editing
  const [currentUserPoint, setCurrentUserPoint] = useState<UserPoint>();

  // disables click events on the map pane itself when true
  // prevents firing both the map's and the feature's click events at the same time
  const [mouseOverFeature, setMouseOverFeature] = useState(Boolean);
  const [userPoints, setUserPoints] = useState<Array<UserPoint>>(
    props.userPoints
  );

  useEffect(() => {
    setUserPoints(props.userPoints);
  }, [props.userPoints]);

  /**
   * Replaces the userPoint at the given index with the new userPoint given as a parameter.
   * Meant for updating data in state.
   * @param {point}
   * */
  const changePoint = (index: number, point: UserPoint) => {
    userPoints[index] = point;
    setUserPoints(userPoints);
    console.log("Changed userPoint", point, "at index", index);
  };

  /**
   * Updates the temporary userpoint in the userPoints list in the state.
   * This updates the map
   */
  const updateNewUserPoint = (point: UserPoint) => {
    let lastUserPoint = userPoints[userPoints.length - 1];
    // only add a new unsaved marker on the map if we haven't done so already
    if (lastUserPoint.id != null) {
      console.log("add new point to map");
      userPoints.push(point);
    } else {
      console.log("move existing 'new' point");
      // otherwise just replace the last unsaved one with the new one we made
      userPoints[userPoints.length - 1] = point;
    }
    //setUserPoints(userPoints);
    console.log("updateNewUserPoint called", point);
    setCurrentUserPoint(point);
  };

  /**
   * Gets the userPoint with the given id from the userPoints list and
   * sets it as the current userPoint to be edited
   * @param {number} id
   */
  const chooseUserPoint = (id: number) => {
    let userPoint = userPoints.find((point) => point.id == id);
    setCurrentUserPoint(userPoint);
    console.log("Calling edit");
    // discard the userPoint that isnt yet in the database
    // if we were in the process of creating one before choosing to instead
    // make an edit to an existing userPoint
    if (userPoints[userPoints.length - 1].id == null) {
      userPoints.pop();
    }
  };

  /**
   * Returns true if the given userPoint is owned by the currently logged in user.
   * @param {UserPoint} point
   * */
  const isOwnUserPoint = (point: UserPoint) => {
    // console.log("Ownership for point", point.id, point.label_text);
    if (!props.user || !point.user) {
      return false;
    }

    return props.user.id == point.user.id;
  };

  /**
   * Returns the correct colour depending on if the point is owned by
   * the currently logged in user or not.
   * @param {UserPoint} point
   **/
  const getUserPointColour = (point: UserPoint) => {
    const ownColour = "#fffb00";
    const otherColour = "#008cff";

    return isOwnUserPoint(point) ? ownColour : otherColour;
  };

  return (
    <div>
      <RMap
        width={"100%"}
        height={"500px"}
        initial={{
          center: fromLonLat([24.94030214683831, 60.1712000939996]),
          zoom: 10,
        }}
        onClick={(e) => {
          if (props.user && !mouseOverFeature) {
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

            updateNewUserPoint(newUserPoint);

            console.log("userpoints", userPoints);
          }
        }}
      >
        <ROSM />
        <RLayerVector zIndex={10}>
          {userPoints.map((point) => {
            return (
              <>
                <RStyle.RStyle>
                  <RStyle.RCircle radius={6}>
                    <RStyle.RStroke
                      color={"#008cff"}
                      width={5}
                    ></RStyle.RStroke>
                    <RStyle.RFill color={"#008cff"}></RStyle.RFill>
                  </RStyle.RCircle>
                </RStyle.RStyle>
                <RFeature
                  key={point.id}
                  geometry={new Point(fromLonLat(point.position.coordinates))}
                  onClick={(e) => {
                    // dig out the userPoint's id from the event
                    let target = e.target;
                    let userPointId = target.getProperties().id;
                    chooseUserPoint(userPointId);

                    return;
                  }}
                  onPointerEnter={() => setMouseOverFeature(true)}
                  onPointerLeave={() => setMouseOverFeature(false)}
                  properties={point}
                >
                  <ROverlay className="example-overlay">
                    {isOwnUserPoint(point) && point.id ? "⭐" : ""}
                    {point.label_text}
                  </ROverlay>
                </RFeature>
              </>
            );
          })}
        </RLayerVector>
        <RInteraction.RTranslate
          onTranslateEnd={(e) => {
            let feature = e.features.item(0);
            let point = feature.getProperties() as UserPoint;
            if (!isOwnUserPoint(point)) {
              return;
            }
            console.log("moved point", point);
            let index = userPoints.findIndex((up) => point.id);

            let newCoords = toLonLat(
              (feature.getGeometry() as Point).getFirstCoordinate()
            );

            point.position.coordinates = newCoords;

            // replace the userPoint in the state
            changePoint(index, point);

            // finally update the userpoint through the API
            userpointService.updateUserPoint(point);
          }}
        />
      </RMap>
      {currentUserPoint ? (
        <NewUserPointForm
          userPoint={currentUserPoint}
          updateNewUserPoint={updateNewUserPoint}
        ></NewUserPointForm>
      ) : !props.user ? (
        <h3>Please log in to add a point.</h3>
      ) : (
        <></>
      )}
    </div>
  );
}
