"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageCircle } from "lucide-react";
import AIAssistantModal from "./AIAssistantModal";

export default function AIAssistantFloatingButton() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const toggleModal = () => {
    setIsModalOpen(!isModalOpen);
  };

  return (
    <>
      {/* Floating AI Assistant Button */}
      <div className="fixed bottom-6 right-6 z-[99]">
        <AnimatePresence>
          <motion.button
            initial={{ scale: 0, y: 20, rotate: -180 }}
            animate={{ scale: 1, y: 0, rotate: 0 }}
            exit={{ scale: 0, y: 20, rotate: -180 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={toggleModal}
            className="w-16 h-16 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg flex items-center justify-center text-white hover:shadow-xl transition-shadow focus:outline-none focus:ring-4 focus:ring-blue-500/50"
            aria-label="Open AI Assistant"
          >
            <motion.div
              animate={{ rotate: isModalOpen ? 180 : 0 }}
              transition={{ duration: 0.2 }}
            >
              <MessageCircle className="w-8 h-8" />
            </motion.div>
          </motion.button>
        </AnimatePresence>
      </div>

      {/* AI Assistant Modal */}
      <AIAssistantModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </>
  );
}
