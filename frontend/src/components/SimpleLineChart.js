import React from 'react';
import {Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from 'recharts';


const SimpleLineChart = (data) => {
    return (
        <div className="chart-container">
            <ResponsiveContainer width="90%" height="90%">
                <LineChart
                    data={data.data}
                    margin={{
                        top: 30,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                >
                    <XAxis dataKey={Object.keys(data.data[0])[0]} />
                    <YAxis dataKey={Object.keys(data.data[0])[1]}/>
                    <Tooltip />
                    <Line
                        type="monotone"
                        dataKey={Object.keys(data.data[0])[2]}
                        stroke="var(--primary-color)"
                        activeDot={{ r: 8 }}
                    />
                    <Line type="monotone" dataKey={Object.keys(data.data[0])[3]} stroke="var(--secondary-color)" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default SimpleLineChart;