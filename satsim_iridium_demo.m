% adapted from matlab website: https://www.mathworks.com/help/aerotbx/ug/satellitescenario.walkerstar.html

startTime = datetime(2020,1,11,14,50,0);
stopTime = startTime + hours(6);
sampleTime = 60;  
sc = satelliteScenario( ...
    startTime,stopTime,sampleTime);

% sc = satelliteScenario;
% Walker-Star constellation with 66 satellites in 6 planes inclined at 86.4 degrees (86.4:66/6/2) in a 781 km orbit
% 6378.14e3 m is the earth's radius
% TODO: randomly choose a satellite
sat = walkerStar(sc, 781e3+6378.14e3, 86.4, 66, 6, 2, Name="Iridium");
% sat = walkerStar(sc, 781e3+6378.14e3, 86.4, 11, 1, 2, Name="Iridium");

sat_positions = zeros(3, 66);
disp("trying to get satellite position");

for i=1:66
    pos = states(sat(i));
    pos_10 = pos(:, 10);
    sat_positions(:, i) = pos_10;
    % disp(pos_10);
end
writematrix(sat_positions, "sat_positions.csv");

% pause

% % add a ground station
% name = "Madrid Deep Space Communications Complex";
% lat1 = 40.43139;                                    % In degrees
% lon1 = -4.24806;                                    % In degrees
% gs1 = groundStation(sc, ...
%     Name=name,Latitude=lat1,Longitude=lon1);
% ac = access(sat, gs1);
% 
% % add a ground station
% name = "user 1";
% lat2 = -32.736349;                                    % In degrees
% lon2 = 21.074430;                                    % In degrees 
% gs2 = groundStation(sc, ...
%     Name=name,Latitude=lat2,Longitude=lon2);
% 
% ac = access(sat, gs2);
% 
% play(sc);
% 
% 
% % satelliteScenarioViewer(sc);
% 
% % Calculate propagation delay from each satellite to the ground station.
% % The latency function internally performs access analysis and returns NaN
% % whenever there is no access.
% [delay1,time1] = latency(sat,gs1);
% [delay2,time2] = latency(sat,gs2);
% 
% % disp(delay);
% 
% % plot(time,delay(1,:)*1000)                  % Plot in milliseconds
% % xlim([time(1) time(end)])
% % title("First Satellite's Latency vs. Time")
% % xlabel("Simulation Time")
% % ylabel("Latency (ms)")
% % grid on
% 
% plot(time1,delay1*1000)                  % Plot in milliseconds
% % xlim([time(1) time(end)])
% title("ground station latency vs. Time")
% xlabel("Simulation Time")
% ylabel("Latency (ms)")
% grid on
% 
% plot(time2,delay2*1000)                  % Plot in milliseconds
% % xlim([time(1) time(end)])
% title("user latency vs. Time")
% xlabel("Simulation Time")
% ylabel("Latency (ms)")
% grid on
