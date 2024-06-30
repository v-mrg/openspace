% adapted from matlab
startTime = datetime(2020,8,19,20,55,0);              % 19 August 2020 8:55 PM UTC
stopTime = startTime + days(1);                       % 20 August 2020 8:55 PM UTC
sampleTime = 60;                                      % seconds
sc = satelliteScenario(startTime,stopTime,sampleTime);

% launch viewer
satelliteScenarioViewer(sc);

% add satellites by specifying their keplerian orbital elements corresponding to the scenario start time
semiMajorAxis = 10000000;                  % meters
eccentricity = 0;
inclination = 0;                           % degrees
rightAscensionOfAscendingNode = 0;         % degrees
argumentOfPeriapsis = 0;                   % degrees
trueAnomaly = 0;                           % degrees
sat1 = satellite(sc, ...
    semiMajorAxis, ...
    eccentricity, ...
    inclination, ...
    rightAscensionOfAscendingNode, ...
    argumentOfPeriapsis, ...
    trueAnomaly, ...
    "Name","Satellite 1", ...
    "OrbitPropagator","two-body-keplerian");

semiMajorAxis = 10000000;                  % meters
eccentricity = 0;
inclination = 30;                          % degrees
rightAscensionOfAscendingNode = 120;       % degrees
argumentOfPeriapsis = 0;                   % degrees
trueAnomaly = 300;                         % degrees
sat2 = satellite(sc, ...
    semiMajorAxis, ...
    eccentricity, ...
    inclination, ...
    rightAscensionOfAscendingNode, ...
    argumentOfPeriapsis, ...
    trueAnomaly, ...
    "Name","Satellite 2", ...
    "OrbitPropagator","two-body-keplerian");

% each satellite consists of two gimbals on opposite end of the spacecraft
% one for the receiver and one for the transmitter
% give rpy mounting locations of the gimabsl on the satellite

gimbalSat1Tx = gimbal(sat1, ...
    "MountingLocation",[0;1;2]);  % meters
gimbalSat2Tx = gimbal(sat2, ...
    "MountingLocation",[0;1;2]);  % meters
gimbalSat1Rx = gimbal(sat1, ...
    "MountingLocation",[0;-1;2]); % meters
gimbalSat2Rx = gimbal(sat2, ...
    "MountingLocation",[0;-1;2]); % meters

% add receivers and transmitters to the gimbals  
sat1Rx = receiver(gimbalSat1Rx, ...
    "MountingLocation",[0;0;1], ...      % meters
    "GainToNoiseTemperatureRatio",3, ... % decibels/Kelvin
    "RequiredEbNo",4);                   % decibels
sat2Rx = receiver(gimbalSat2Rx, ...
    "MountingLocation",[0;0;1], ...      % meters
    "GainToNoiseTemperatureRatio",3, ... % decibels/Kelvin
    "RequiredEbNo",4);                   % decibels

% gaussianantenna sets the dish diameter of the receiver antennas
gaussianAntenna(sat1Rx, ...
    "DishDiameter",0.5);    % meters
gaussianAntenna(sat2Rx, ...
    "DishDiameter",0.5);    % meters

% add transmitters to the gimbals
% sat1 transmitter is used for crosslink to sat2 in this case
sat1Tx = transmitter(gimbalSat1Tx, ...
    "MountingLocation",[0;0;1], ...   % meters
    "Frequency",30e9, ...             % hertz
    "Power",15);                      % decibel watts
sat2Tx = transmitter(gimbalSat2Tx, ...
    "MountingLocation",[0;0;1], ...   % meters
    "Frequency",27e9, ...             % hertz
    "Power",15);                      % decibel watts

% specify that the transmitter antennas are also gaussian antennas
gaussianAntenna(sat1Tx, ...
    "DishDiameter",0.5);    % meters
gaussianAntenna(sat2Tx, ...
    "DishDiameter",0.5);    % meters

% add groundstations by latitude & longitude coordinates
latitude = 12.9436963;          % degrees
longitude = 77.6906568;         % degrees
gs1 = groundStation(sc, ...
    latitude, ...
    longitude, ...
    "Name","Ground Station 1");


latitude = -33.7974039;        % degrees
longitude = 151.1768208;       % degrees
gs2 = groundStation(sc, ...
    latitude, ...
    longitude, ...
    "Name","Ground Station 2");

% add gimbal to each groundstation
% in this case, GS 1 has a transmitter and GS2 has a receiver
% gimbals are located 5m above the GS
% mounting angles of the gimbals align the body axes with the parent
% when gimbals are not steered, the z_g axis points straight down, along with the antenna attached to it using default mounting angles
% so we must set the mounting pitch angle to 180deg go that z_g points straight up when the gimbal is not steered

gimbalGs1 = gimbal(gs1, ...
    "MountingAngles",[0;180;0], ... % degrees
    "MountingLocation",[0;0;-5]);   % meters
gimbalGs2 = gimbal(gs2, ...
    "MountingAngles",[0;180;0], ... % degrees
    "MountingLocation",[0;0;-5]);   % meters

% add transmitters to GS1 gimbal
gs1Tx = transmitter(gimbalGs1, ...
    "Name","Ground Station 1 Transmitter", ...
    "MountingLocation",[0;0;1], ...           % meters
    "Frequency",30e9, ...                     % hertz
    "Power",30);                              % decibel watts

% define it as a gaussian antenna
gaussianAntenna(gs1Tx, ...
    "DishDiameter",2); % meters

% add receiver to GS2 gimbal
gs2Rx = receiver(gimbalGs2, ...
    "Name","Ground Station 2 Receiver", ...
    "MountingLocation",[0;0;1], ...        % meters
    "GainToNoiseTemperatureRatio",3, ...   % decibels/Kelvin
    "RequiredEbNo",1);                     % decibels

% define it as a gaussian antenna
gaussianAntenna(gs2Rx, ...
    "DishDiameter",2); % meters

% antennas need to continuously point at their respective targets
% by setting a target, the z_g axis of the gimbal will track the target
pointAt(gimbalGs1,sat1);
pointAt(gimbalSat1Rx,gs1);
pointAt(gimbalSat1Tx,sat2);
pointAt(gimbalSat2Rx,sat1);
pointAt(gimbalSat2Tx,gs2);
pointAt(gimbalGs2,sat2);

% add link analysis to the transmitter at GS 1 
% link is a regenerative repeater-type that originates at gs1tx and ends at
% GS2TX, routed through sat1rx, sat2rx, and sat2tx
lnk = link(gs1Tx,sat1Rx,sat1Tx,sat2Rx,sat2Tx,gs2Rx);

% define times when link is closed
% this function generates a table showing when GS1 can send data to GS2
linkIntervals(lnk);

% during play, the green lines disappear whenever the link cannot be closed
play(sc);
