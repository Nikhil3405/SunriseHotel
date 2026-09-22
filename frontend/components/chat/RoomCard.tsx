import { BedDouble, Check, Users } from "lucide-react";
import type { AvailableRoom } from "@/types/chat";

type RoomCardProps = {
  room: AvailableRoom;
};

export default function RoomCard({ room }: RoomCardProps) {
  return (
    <div className="rounded-2xl border border-[#E7E5E4] bg-white p-4 shadow-sm">
      <div className="mb-3">
        <h3 className="font-semibold text-[#292524]">
          {room.name}
        </h3>

        <p className="mt-1 text-sm leading-5 text-[#78716C]">
          {room.description}
        </p>
      </div>

      <div className="space-y-2 text-sm text-[#57534E]">
        <div className="flex items-center gap-2">
          <BedDouble
            className="h-4 w-4 shrink-0"
            aria-hidden="true"
          />
          <span>{room.beds}</span>
        </div>

        <div className="flex items-center gap-2">
          <Users
            className="h-4 w-4 shrink-0"
            aria-hidden="true"
          />
          <span>Up to {room.max_guests} guests</span>
        </div>
      </div>

      <div className="mt-4 flex items-end justify-between gap-3 border-t border-[#F5F5F4] pt-3">
        <div>
          <span className="text-lg font-semibold text-[#292524]">
            ₹{room.price_per_night.toLocaleString("en-IN")}
          </span>

          <span className="ml-1 text-xs text-[#78716C]">
            / night
          </span>
        </div>

        {room.breakfast_included && (
          <div className="flex items-center gap-1 text-xs font-medium text-[#15803D]">
            <Check
              className="h-4 w-4 shrink-0"
              aria-hidden="true"
            />
            <span>Breakfast included</span>
          </div>
        )}
      </div>
    </div>
  );
}