"""
Fair Use Assessor Module
Evaluates whether content qualifies for educational fair use under US copyright law
"""


class FairUseAssessor:
    """
    Assesses fair use for educational purposes based on the four factors:
    1. Purpose and character of use
    2. Nature of the copyrighted work
    3. Amount and substantiality used
    4. Effect on market value
    """

    def __init__(self):
        self.factor_weights = {
            'purpose': 0.25,
            'nature': 0.25,
            'amount': 0.25,
            'market_effect': 0.25
        }

    def assess(self, copyright_info, course_type, institution_type, content_type):
        """
        Assess fair use for educational content

        Args:
            copyright_info: Dictionary with copyright/license information
            course_type: Type of course (online, hybrid, in-person)
            institution_type: Type of institution (university, K-12, etc)
            content_type: Type of content (image, document, video, etc)

        Returns:
            Dictionary with fair use assessment
        """
        assessment = {
            'can_use': None,
            'confidence': 'Medium',
            'factors': {},
            'recommendation': '',
            'warnings': [],
            'best_practices': []
        }

        # If content is public domain or openly licensed, no fair use needed
        if copyright_info.get('is_public_domain'):
            assessment['can_use'] = True
            assessment['confidence'] = 'High'
            assessment['recommendation'] = (
                'This content is in the public domain and can be freely used '
                'without restrictions.'
            )
            return assessment

        if self._is_open_license(copyright_info):
            assessment['can_use'] = True
            assessment['confidence'] = 'High'
            assessment['recommendation'] = self._generate_open_license_recommendation(
                copyright_info
            )
            return assessment

        # Perform four-factor analysis
        factor_scores = {}

        # Factor 1: Purpose and Character
        factor_scores['purpose'] = self._assess_purpose(
            course_type,
            institution_type
        )

        # Factor 2: Nature of Work
        factor_scores['nature'] = self._assess_nature(
            content_type,
            copyright_info
        )

        # Factor 3: Amount and Substantiality
        factor_scores['amount'] = self._assess_amount(
            content_type,
            copyright_info
        )

        # Factor 4: Effect on Market
        factor_scores['market_effect'] = self._assess_market_effect(
            course_type,
            institution_type,
            content_type
        )

        # Calculate weighted score
        total_score = sum(
            factor_scores[factor] * self.factor_weights[factor]
            for factor in factor_scores
        )

        # Determine if use is likely fair
        if total_score >= 0.7:
            assessment['can_use'] = True
            assessment['confidence'] = 'High'
        elif total_score >= 0.5:
            assessment['can_use'] = True
            assessment['confidence'] = 'Medium'
            assessment['warnings'].append(
                'Fair use is likely but not certain. Consider seeking legal advice.'
            )
        elif total_score >= 0.3:
            assessment['can_use'] = False
            assessment['confidence'] = 'Medium'
            assessment['warnings'].append(
                'Fair use is uncertain. Strongly recommend seeking permission or alternatives.'
            )
        else:
            assessment['can_use'] = False
            assessment['confidence'] = 'High'

        # Add factor details to assessment
        assessment['factors'] = self._format_factors(factor_scores)

        # Generate recommendation
        assessment['recommendation'] = self._generate_recommendation(
            assessment['can_use'],
            total_score,
            copyright_info,
            course_type
        )

        # Add best practices
        assessment['best_practices'] = self._get_best_practices(
            copyright_info,
            course_type
        )

        return assessment

    def _assess_purpose(self, course_type, institution_type):
        """
        Assess Factor 1: Purpose and Character of Use
        Educational use generally favors fair use
        """
        score = 0.0
        details = []

        # Nonprofit educational use
        if institution_type in ['Public University', 'Community College', 'K-12']:
            score += 0.5
            details.append('✓ Nonprofit educational institution')
        else:
            score += 0.3
            details.append('~ Private institution (still educational)')

        # Transformative use
        score += 0.3
        details.append('✓ Teaching is transformative (adds educational value)')

        # Limited distribution
        if course_type in ['In-person', 'Hybrid']:
            score += 0.2
            details.append('✓ Limited to enrolled students')
        else:
            score += 0.1
            details.append('~ Online distribution (wider access)')

        return min(score, 1.0)

    def _assess_nature(self, content_type, copyright_info):
        """
        Assess Factor 2: Nature of the Copyrighted Work
        Factual/published works favor fair use more than creative/unpublished
        """
        score = 0.0
        details = []

        # Published vs unpublished
        score += 0.4
        details.append('✓ Assuming published work')

        # Type of work
        if content_type in ['document', 'pdf', 'txt']:
            # Text can be factual or creative
            score += 0.3
            details.append('~ Textual content (varies by nature)')
        elif content_type in ['image', 'jpg', 'png', 'gif']:
            # Images tend to be more creative
            score += 0.2
            details.append('~ Visual content (often creative)')

        return min(score, 1.0)

    def _assess_amount(self, content_type, copyright_info):
        """
        Assess Factor 3: Amount and Substantiality of Use
        Using less favors fair use
        """
        score = 0.0
        details = []

        if content_type in ['image', 'jpg', 'jpeg', 'png', 'gif']:
            # For images, using the whole image is often necessary
            score += 0.5
            details.append(
                '~ Using complete image (may be necessary for educational purpose)'
            )
        else:
            # For documents, assuming excerpts
            score += 0.7
            details.append(
                '✓ Assuming use of excerpts rather than entire work'
            )

        # Not using "heart" of the work
        score += 0.3
        details.append('✓ Educational use typically doesn\'t exploit commercial core')

        return min(score, 1.0)

    def _assess_market_effect(self, course_type, institution_type, content_type):
        """
        Assess Factor 4: Effect on Market Value
        Negative impact on market disfavors fair use
        """
        score = 0.0
        details = []

        # Educational use typically doesn't replace market
        score += 0.5
        details.append('✓ Educational use doesn\'t typically replace purchase')

        # Limited audience
        if course_type in ['In-person', 'Hybrid']:
            score += 0.3
            details.append('✓ Limited to course participants')
        else:
            score += 0.2
            details.append('~ Online course (wider potential distribution)')

        # No commercial benefit
        score += 0.2
        details.append('✓ No commercial benefit to institution')

        return min(score, 1.0)

    def _is_open_license(self, copyright_info):
        """Check if content has an open license"""
        if not copyright_info:
            return False

        license_type = copyright_info.get('license_type', '')
        if not license_type:
            return False

        open_indicators = [
            'creative commons',
            'cc by',
            'cc0',
            'public domain',
            'open',
        ]

        return any(
            indicator in license_type.lower()
            for indicator in open_indicators
        )

    def _format_factors(self, factor_scores):
        """Format factor scores for display"""
        formatted = {}

        # Factor 1
        purpose_score = factor_scores['purpose']
        if purpose_score >= 0.7:
            formatted['purpose'] = '✓ Strongly favors fair use (nonprofit educational purpose)'
        elif purpose_score >= 0.5:
            formatted['purpose'] = '~ Moderately favors fair use (educational purpose)'
        else:
            formatted['purpose'] = '✗ Does not favor fair use'

        # Factor 2
        nature_score = factor_scores['nature']
        if nature_score >= 0.7:
            formatted['nature'] = '✓ Favors fair use (factual/informational work)'
        elif nature_score >= 0.5:
            formatted['nature'] = '~ Neutral (published work)'
        else:
            formatted['nature'] = '✗ Does not favor fair use (highly creative work)'

        # Factor 3
        amount_score = factor_scores['amount']
        if amount_score >= 0.7:
            formatted['amount'] = '✓ Favors fair use (limited portion used)'
        elif amount_score >= 0.5:
            formatted['amount'] = '~ Neutral (reasonable amount for educational purpose)'
        else:
            formatted['amount'] = '✗ Does not favor fair use (substantial portion used)'

        # Factor 4
        market_score = factor_scores['market_effect']
        if market_score >= 0.7:
            formatted['market_effect'] = '✓ Favors fair use (no market harm)'
        elif market_score >= 0.5:
            formatted['market_effect'] = '~ Neutral (minimal market impact)'
        else:
            formatted['market_effect'] = '✗ Does not favor fair use (potential market harm)'

        return formatted

    def _generate_recommendation(self, can_use, score, copyright_info, course_type):
        """Generate detailed recommendation"""

        if can_use:
            recommendation = (
                f'**Fair Use Likely Applies** (Score: {score:.2f})\n\n'
                'Based on the four-factor analysis, this use likely qualifies as fair use '
                'for educational purposes. However, fair use is determined on a case-by-case basis.\n\n'
                '**Recommendations:**\n'
                '- Use only what is necessary for educational purpose\n'
                '- Provide proper attribution to the original creator\n'
                '- Limit access to enrolled students only\n'
                '- Include copyright notice and disclaimer\n'
                '- Do not make publicly accessible\n\n'
            )

            if score < 0.6:
                recommendation += (
                    '**Caution:** Fair use is not certain in this case. '
                    'Consider seeking permission or using licensed alternatives.'
                )

        else:
            recommendation = (
                f'**Fair Use Unlikely** (Score: {score:.2f})\n\n'
                'Based on the four-factor analysis, this use may not qualify as fair use.\n\n'
                '**Recommendations:**\n'
                '- Seek permission from the copyright holder\n'
                '- Use licensed alternatives (see suggestions)\n'
                '- Use only brief excerpts with permission\n'
                '- Consider public domain or Creative Commons alternatives\n\n'
            )

        # Add course-specific guidance
        if course_type == 'Online':
            recommendation += (
                '\n**Note for Online Courses:**\n'
                'Online distribution may face stricter fair use scrutiny. '
                'Use password-protected learning management systems and '
                'limit access to enrolled students only.'
            )

        return recommendation

    def _generate_open_license_recommendation(self, copyright_info):
        """Generate recommendation for openly licensed content"""

        license_type = copyright_info.get('license_type', 'Open License')

        recommendation = (
            f'**{license_type}**\n\n'
            'This content is openly licensed and can be used in your course.\n\n'
        )

        if copyright_info.get('attribution_required'):
            recommendation += (
                '**Attribution Required:**\n'
                'You must provide proper attribution to the original creator.\n'
            )
            if copyright_info.get('attribution_text'):
                recommendation += f'\n```\n{copyright_info["attribution_text"]}\n```\n\n'

        if not copyright_info.get('commercial_use_allowed'):
            recommendation += (
                '**⚠️ Non-Commercial Only:**\n'
                'This license restricts use to non-commercial purposes only. '
                'Educational use typically qualifies.\n\n'
            )

        if not copyright_info.get('modifications_allowed'):
            recommendation += (
                '**⚠️ No Derivatives:**\n'
                'This license does not allow modifications. Use the content as-is.\n\n'
            )

        if copyright_info.get('restrictions'):
            recommendation += '**Restrictions:**\n'
            for restriction in copyright_info['restrictions']:
                recommendation += f'- {restriction}\n'

        return recommendation

    def _get_best_practices(self, copyright_info, course_type):
        """Get list of best practices for using the content"""

        practices = [
            'Provide clear attribution to the original creator/source',
            'Use only the amount necessary for your educational purpose',
            'Include a copyright disclaimer in your course materials',
            'Limit access to enrolled students only (use LMS password protection)',
            'Keep records of your fair use reasoning',
            'Review usage annually and update as needed',
        ]

        if course_type == 'Online':
            practices.extend([
                'Use DRM or access controls to prevent downloading',
                'Include copyright notice on each page/screen',
                'Consider time-limited access (remove at end of term)',
            ])

        if copyright_info and copyright_info.get('attribution_required'):
            practices.insert(0, 'REQUIRED: Provide attribution as specified by the license')

        return practices


def generate_attribution(author, title, license_type, source_url=None):
    """Helper function to generate proper attribution text"""

    attribution = f'"{title}" by {author}'

    if license_type:
        attribution += f' is licensed under {license_type}'

    if source_url:
        attribution += f'. Available at: {source_url}'

    return attribution
