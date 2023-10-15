import Map from "ol/Map";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { useGeographic } from "ol/proj";
// Import - Import for Controls
import ScaleLineControl from "ol/control/ScaleLine";
import FullScreenControl from "ol/control/FullScreen";
import {
  Zoom,
  Attribution,
  Rotate,
  MousePosition,
  ZoomSlider,
} from "ol/control";

// Import - Import for function that creates cordinates
import { createStringXY } from "ol/coordinate";
import { View } from "ol";
import React from "react";

export interface IMapViewProps {}

export default function MapView(props: IMapViewProps) {
  const rotateControl = new Rotate();
  const zoomSliderControl = new ZoomSlider();
  const scaleLineControl = new ScaleLineControl();
  const fullScreenControl = new FullScreenControl();
  const attrControl = new Attribution();
  const zoomControl = new Zoom({});
  const mousePositionControl = new MousePosition({
    coordinateFormat: createStringXY(4),
    projection: "EPSG:4326",
    className: "custom-mouse-position",
  });

  // State inizialization - State for Map ref and Map
  const mapTargetElement = React.useRef<HTMLDivElement>(null);
  const [map, setMap] = React.useState<Map | undefined>();
  useGeographic();
  React.useEffect(() => {
    const map = new Map({
      layers: [new TileLayer({ source: new OSM() })],
      controls: [],
      view: new View({
        center: [24.936870712, 60.18904722],
        zoom: 7,
        minZoom: 0,
        maxZoom: 28,
      }),
    });
    map.setTarget(mapTargetElement.current || "");
    setMap(map);
    map.getView().setCenter([24.936870712, 60.18904722]);

    return () => map.setTarget("");
  }, []);

  return (
    <>
      <div
        ref={mapTargetElement}
        className="map"
        style={{
          width: "100%",
          height: "400px",
          position: "relative",
        }}
      ></div>
    </>
  );
}
