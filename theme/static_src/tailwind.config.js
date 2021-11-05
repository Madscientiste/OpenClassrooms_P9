const colors = require("tailwindcss/colors");
const defaultConfig = require("tailwindcss/defaultConfig");

module.exports = {
	/**
	 * Stylesheet generation mode.
	 *
	 * Set mode to "jit" if you want to generate your styles on-demand as you author your templates;
	 * Set mode to "aot" if you want to generate the stylesheet in advance and purge later (aka legacy mode).
	 */
	mode: "jit",

	purge: [
		/**
		 * HTML. Paths to Django template files that will contain Tailwind CSS classes.
		 */

		/*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
		"../templates/**/*.html",

		/*
		 * Main templates directory of the project (BASE_DIR/templates).
		 * Adjust the following line to match your project structure.
		 */
		"../../templates/**/*.html",

		/*
		 * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
		 * Adjust the following line to match your project structure.
		 */
		"../../**/templates/**/*.html",

		/**
		 * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
		 * patterns match your project structure.
		 */
		/* JS 1: Ignore any JavaScript in node_modules folder. */
		// '!../../**/node_modules',
		/* JS 2: Process all JavaScript files in the project. */
		// '../../**/*.js',

		/**
		 * Python: If you use Tailwind CSS classes in Python, uncomment the following line
		 * and make sure the pattern below matches your project structure.
		 */
		// '../../**/*.py'
	],
	darkMode: false, // or 'media' or 'class'
	theme: {
		colors: {
			primary: "#F7813F",
			secondary: "#788CF4",
			layer: "rgba(255, 255, 255, 10%)",
			light: "#FFFFFF",
			dimm: "#837C7C",
			dark: {
				100: "#0E0B0B",
				200: "#292929",
			},
		},

		flex: {
			1: "1 1 0%",
			auto: "1 1 auto",
			initial: "0 1 auto",
			inherit: "inherit",
			none: "none",

			100: "1 1 100%",
			75: "1 1 75%",
			50: "1 1 50%",
			25: "1 1 25%",
			0: "1 1 0%",
		},

		fontFamily: {
			body: ["Inter"],
		},
	},
	variants: {
		extend: {},
	},
	plugins: [
		require("@tailwindcss/forms"),
		require("@tailwindcss/typography"),
		require("@tailwindcss/line-clamp"),
		require("@tailwindcss/aspect-ratio"),
	],
};
