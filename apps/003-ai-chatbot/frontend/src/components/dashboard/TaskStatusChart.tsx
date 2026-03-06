"use client";

import { motion } from "framer-motion";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

interface TaskStatusChartProps {
  completed: number;
  pending: number;
  inProgress?: number;
}

interface ChartData {
  name: string;
  value: number;
  color: string;
  [key: string]: string | number;
}

export default function TaskStatusChart({
  completed,
  pending,
  inProgress = 0,
}: TaskStatusChartProps) {
  const data: ChartData[] = [
    { name: "Completed", value: completed, color: "#22c55e" },
    { name: "Pending", value: pending, color: "#eab308" },
  ];

  if (inProgress > 0) {
    data.push({ name: "In Progress", value: inProgress, color: "#3b82f6" });
  }

  const total = completed + pending + inProgress;

  // Don't render if no data
  if (total === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-100 dark:border-gray-700"
      >
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-4">
          Task Status
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
      transition={{ duration: 0.4, delay: 0.2 }}
      className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-100 dark:border-gray-700"
    >
      <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-4">
        Task Status
      </h3>

      <div className="relative h-48">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={45}
              outerRadius={70}
              paddingAngle={3}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} stroke="none" />
              ))}
            </Pie>
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
          </PieChart>
        </ResponsiveContainer>

        {/* Center text */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
              {total}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">Total</p>
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="flex justify-center gap-4 mt-4">
        {data.map((item) => (
          <div key={item.name} className="flex items-center gap-2">
            <div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: item.color }}
            />
            <span className="text-xs text-gray-600 dark:text-gray-400">
              {item.name}
            </span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
