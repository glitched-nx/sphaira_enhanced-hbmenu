#pragma once

#include "ui/widget.hpp"
#include <optional>

namespace sphaira::ui {

class ErrorBox final : public Widget {
public:
    ErrorBox(Result code, const std::string& message);
    ErrorBox(const std::string& message);

    auto Update(Controller* controller, TouchInfo* touch) -> void override;
    auto Draw(NVGcontext* vg, Theme* theme) -> void override;

private:
    std::optional<Result> m_code{};
    std::string m_message{};
    std::string m_code_message{};
    std::string m_code_module{};
};

} // namespace sphaira::ui
