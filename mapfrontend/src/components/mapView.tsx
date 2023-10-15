import React, { useState } from "react";
import { UserPoint } from "../classes/userpoint";

import { fromLonLat, toLonLat } from "ol/proj";
import { Point } from "ol/geom";
import "ol/ol.css";

import { RMap, ROSM, RLayerVector, RFeature, ROverlay, RStyle } from "rlayers";
//import locationIcon from "./svg/location.svg";

export interface IMapViewProps {
  userPoints: Array<UserPoint>;
}

export default function MapView(props: IMapViewProps) {
  const [newUserPoint, setNewUserPoint] = useState<UserPoint>();

  return (
    <RMap
      className="example-map"
      width={"100%"}
      height={"500px"}
      initial={{
        center: fromLonLat([24.94030214683831, 60.1712000939996]),
        zoom: 10,
      }}
      onClick={(e) => {
        const coords = e.map.getCoordinateFromPixel(e.pixel);
      }}
    >
      <ROSM />
      <RLayerVector zIndex={10}>
        <RStyle.RStyle></RStyle.RStyle>
        {props.userPoints.map((point) => (
          <RFeature
            geometry={new Point(fromLonLat(point.position.coordinates))}
          >
            <ROverlay className="example-overlay">{point.label_text}</ROverlay>
          </RFeature>
        ))}
      </RLayerVector>
    </RMap>
  );
}
