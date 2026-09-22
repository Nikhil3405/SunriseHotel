import Image from "next/image";

type SunriseLogoProps = {
  size?: "sm" | "md" | "lg";
  showName?: boolean;
};

const sizes = {
  sm: 34,
  md: 42,
  lg: 54,
};

export default function SunriseLogo({
  size = "md",
  showName = false,
}: SunriseLogoProps) {
  const logoSize = sizes[size];

  return (
    <div className="flex items-center gap-3">
      <div className="flex shrink-0 items-center justify-center">
        <Image
          src="/logo.svg"
          alt="Sunrise Hotel"
          width={logoSize}
          height={logoSize}
          priority
        />
      </div>

      {showName && (
        <div className="leading-tight">
          <h1 className="text-[15px] font-semibold tracking-tight text-[#292524] sm:text-base">
            Sunrise Hotel
          </h1>
          <p className=" text-[11px] text-[#A8A29E]">
            Your stay, made simple
          </p>
        </div>
      )}
    </div>
  );
}