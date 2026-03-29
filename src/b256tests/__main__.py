from b256tests import generators


def main() -> int:
    return generators.main()  # type: ignore[no-any-return]


if __name__ == "__main__":
    raise SystemExit(main())
