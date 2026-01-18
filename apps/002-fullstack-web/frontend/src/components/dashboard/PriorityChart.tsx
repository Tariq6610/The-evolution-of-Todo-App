"use client";

import { motion } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

interface PriorityChartProps {
  high: number;
  medium: number;
  low: number;
}

interface ChartData {
  name: string;
  value: number;
  color: string;
}

const PRIORITY_COLORS = {
  HIGH: "#ef4444",
  MEDIUM: "#eab308",
  LOW: "#22c55e",
};

export default function PriorityChart({
  high,
  medium,
  low,
}: PriorityChartProps) {
  const data: ChartData[] = [
    { name: "High", value: high, color: PRIORITY_COLORS.HIGH },
    { name: "Medium", value: medium, color: PRIORITY_COLORS.MEDIUM },
    { name: "Low", value: low, color: PRIORITY_COLORS.LOW },
  ];

  const total = high + medium + low;

  // Don't render if no data
  if (total === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-100 dark:border-gray-700"
      >
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-4">
          Priority Distribution
        </h3>
        <div className="h-48 flex items-center justify-center text-gray-400 text-sm">
          No tasks yet
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4, delay: 0.3 }}
      className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-100 dark:border-gray-700"
    >
      <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-4">
        Priority Distribution
      </h3>

      <div className="h-48">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
          >
            <XAxis
              dataKey="name"
              axisLine={false}
              tickLine={false}
              tick={{
                fontSize: 12,
                fill: "#6b7280",
              }}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{
                fontSize: 12,
                fill: "#6b7280",
              }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(255,255,255,0.95)",
                border: "none",
                borderRadius: "8px",
                boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
              }}
              formatter={(value: number | undefined) => [
                `${value ?? 0} tasks`,
                "",
              ]}
            />
            <Bar dataKey="value" radius={[6, 6, 0, 0]} animationDuration={1000}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  );
}
